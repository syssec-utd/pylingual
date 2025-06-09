from pika import BasicProperties
from pika.exceptions import ChannelClosedByBroker
from petisco.event.bus.domain.interface_event_bus import IEventBus
from petisco.event.configurer.infrastructure.rabbitmq_event_configurer import RabbitMqEventConfigurer
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_consumer_connector import RabbitMqConsumerConnector
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_event_queue_name_formatter import RabbitMqEventQueueNameFormatter
from petisco.event.shared.domain.event import Event

class RabbitMqConsumerEventBus(IEventBus):

    def __init__(self, connector: RabbitMqConsumerConnector, organization: str, service: str):
        self.connector = connector
        self.exchange_name = f'{organization}.{service}'
        self.rabbitmq_key = f'publisher-{self.exchange_name}'
        self.configurer = RabbitMqEventConfigurer(connector, organization, service)
        self.properties = BasicProperties(delivery_mode=2)

    def publish(self, event: Event):
        if hasattr(self, 'info_id'):
            event = event.add_info_id(self.info_id)
        if not event or not issubclass(event.__class__, Event):
            raise TypeError('Bus only publishes petisco.Event objects')
        try:
            channel = self.connector.get_channel(self.rabbitmq_key)
            routing_key = RabbitMqEventQueueNameFormatter.format(event, exchange_name=self.exchange_name)
            channel.basic_publish(exchange=self.exchange_name, routing_key=routing_key, body=event.to_json(), properties=self.properties)
        except ChannelClosedByBroker:
            self.configurer.configure_event(event)
            self.publish(event)

    def retry_publish_only_on_store_queue(self, event: Event):
        if not event or not issubclass(event.__class__, Event):
            raise TypeError('Bus only publishes petisco.Event objects')
        channel = self.connector.get_channel(self.rabbitmq_key)
        channel.basic_publish(exchange=self.exchange_name, routing_key='retry.store', body=event.to_json(), properties=self.properties)

    def close(self):
        self.connector.close(self.rabbitmq_key)