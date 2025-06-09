def publish(self, project, topic, messages):
    """Publishes messages to a Pub/Sub topic.

        :param project: the GCP project ID in which to publish
        :type project: str
        :param topic: the Pub/Sub topic to which to publish; do not
            include the ``projects/{project}/topics/`` prefix.
        :type topic: str
        :param messages: messages to publish; if the data field in a
            message is set, it should already be base64 encoded.
        :type messages: list of PubSub messages; see
            http://cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage
        """
    body = {'messages': messages}
    full_topic = _format_topic(project, topic)
    request = self.get_conn().projects().topics().publish(topic=full_topic, body=body)
    try:
        request.execute(num_retries=self.num_retries)
    except HttpError as e:
        raise PubSubException('Error publishing to topic {}'.format(full_topic), e)