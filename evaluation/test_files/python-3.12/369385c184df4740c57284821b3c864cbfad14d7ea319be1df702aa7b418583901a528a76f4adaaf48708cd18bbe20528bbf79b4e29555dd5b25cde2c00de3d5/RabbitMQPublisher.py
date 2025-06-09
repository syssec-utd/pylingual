from typing import Any, List, Optional
from pika.exchange_type import ExchangeType
from returns.curry import partial
from returns.functions import tap
from returns.future import FutureFailure, FutureResult, FutureSuccess
from returns.iterables import Fold
from returns.maybe import Maybe
from returns.pipeline import flow, managed, pipe
from returns.pointfree import bind, map_
from returns.result import Result, Success
from dino_seedwork_be.adapters.messaging.notification import Notification, NotificationPublisher, NotificationSerializer, PublishedNotificationTrackerStore
from dino_seedwork_be.adapters.persistance.sql.DBSessionUser import SuperDBSessionUser
from dino_seedwork_be.domain.event.EventSerializer import EventSerializer
from dino_seedwork_be.domain.event.EventStore import EventStore
from dino_seedwork_be.domain.event.StoredEvent import StoredEvent
from dino_seedwork_be.exceptions import MainException
from dino_seedwork_be.utils import feed_args, feed_kwargs, print_result_with_text
from dino_seedwork_be.utils.functional import return_v
from . import RabbitMQConnectionSettings, RabbitMQExchange, RabbitMQMessageParameters, RabbitMQMessageProducer

class RabbitMQPublisher(NotificationPublisher, SuperDBSessionUser):
    _event_store: EventStore
    _exchange_name: str
    _exchange_type: ExchangeType
    _published_notif_tracker_store: PublishedNotificationTrackerStore
    _message_producer_ins: Optional[RabbitMQMessageProducer] = None
    _event_serializer: EventSerializer
    _connection_settings: RabbitMQConnectionSettings

    def __init__(self, event_store: EventStore, exchange_name: str, exchange_type: ExchangeType, published_notif_tracker_store: PublishedNotificationTrackerStore, event_serializer: EventSerializer, connection_settings: RabbitMQConnectionSettings) -> None:
        self.set_exchange_name(exchange_name)
        self.set_event_store(event_store)
        self._connection_settings = connection_settings

        def init_message_producer():
            self._exchange_type = exchange_type
            self._message_producer()
        init_message_producer()
        self.set_published_notif_tracker_store(published_notif_tracker_store)
        self.set_session_users([self.event_store(), self.published_notif_tracker_store()])
        self._event_serializer = event_serializer
        super().__init__()

    def event_serializer(self):
        return self._event_serializer

    def publish_notifications(self) -> FutureResult[Maybe[int], Any]:
        """
        publish unpublished event in event store
        :return: return the last event int id that published already
        """

        def notifications_from(events: List[StoredEvent]) -> Result[List[Notification], Any]:
            return flow(events, partial(map, lambda stored_event: flow(None, lambda _: self.event_serializer().deserialize(stored_event.body()), map_(lambda domain_event: list([stored_event.id().value_or(None), domain_event])), bind(feed_args(Notification.factory)))), list, lambda results: Fold.collect(results, Success(())))

        def publish_future(msg_producer: RabbitMQMessageProducer) -> FutureResult[Maybe[int], Any]:
            match msg_producer.is_ready_for_publish():
                case False:
                    return FutureFailure(MainException('RabbitMQMessageProducer not ready yet'))
                case True:
                    return self.published_notif_tracker_store().published_notification_tracker().bind(lambda tracker: flow(tracker.most_recent_published_notification_id().value_or(0), self.event_store().all_stored_events_since, bind(pipe(notifications_from, FutureResult.from_result)), map_(print_result_with_text('notification from results')), bind(pipe(partial(map, lambda notif: flow(notif, partial(self._publish, msg_producer), map_(return_v(notif)))), lambda publish_results: Fold.collect(publish_results, FutureSuccess(())))), bind(partial(self.published_notif_tracker_store().track_most_recent_published_notification, tracker))))

        def close_producer(producer: RabbitMQMessageProducer, _):
            producer.close()
            return FutureSuccess(None)
        return managed(publish_future, close_producer)(FutureResult.from_result(self._message_producer()))

    def _notification_routing_key(self, notification: Notification):
        return notification.type_name()

    def _publish(self, a_message_producer: RabbitMQMessageProducer, a_notification: Notification) -> FutureResult[None, Exception]:
        return flow({'a_type': a_notification.type_name(), 'a_message_id': str(a_notification.id()), 'a_timestamp': int(a_notification.occurred_on().timestamp())}, feed_kwargs(RabbitMQMessageParameters.durable_text_parameters), lambda text_parameters: flow(a_notification, NotificationSerializer.instance().serialize, map_(tap(print_result_with_text('notification serialized'))), lambda notif_string: FutureResult.from_result(a_message_producer.send(text_parameters, notif_string, self._notification_routing_key(a_notification)))))

    def event_store(self) -> EventStore:
        return self._event_store

    def exchange_name(self) -> str:
        return self._exchange_name

    def exchange_type(self) -> ExchangeType:
        return self._exchange_type

    def published_notif_tracker_store(self) -> PublishedNotificationTrackerStore:
        return self._published_notif_tracker_store

    def set_event_store(self, event_store: EventStore):
        self._event_store = event_store

    def set_exchange_name(self, a_name: str):
        self._exchange_name = a_name

    def _set_message_producer(self, message_producer: RabbitMQMessageProducer):
        self._message_producer_ins = message_producer

    def _message_producer(self) -> Result[RabbitMQMessageProducer, Any]:
        match self._message_producer_ins:
            case None:
                return flow([self._connection_settings, self.exchange_name(), self.exchange_type(), True], feed_args(RabbitMQExchange.factory), map_(RabbitMQMessageProducer.factory), map_(tap(self._set_message_producer)))
            case RabbitMQMessageProducer():
                return Success(self._message_producer_ins)
            case _:
                print('not message producer in case', self._message_producer_ins)

    def set_published_notif_tracker_store(self, a_published_notif_tracker_store: PublishedNotificationTrackerStore):
        self._published_notif_tracker_store = a_published_notif_tracker_store

    def run(self):
        self._message_producer().unwrap().run()

    def is_ready(self) -> Result[bool, Any]:
        return self._message_producer().map(lambda producer: producer.is_ready_for_publish()).lash(lambda _: Success(False))

    def get_last_published_notification_id(self) -> FutureResult[Maybe[int], Any]:
        return self.published_notif_tracker_store().published_notification_tracker().map(lambda tracker: tracker.most_recent_published_notification_id())