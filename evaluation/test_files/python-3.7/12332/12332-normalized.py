def write(self, obj, resource_id=None):
    """Write obj in elasticsearch.
        :param obj: value to be written in elasticsearch.
        :param resource_id: id for the resource.
        :return: id of the transaction.
        """
    self.logger.debug('elasticsearch::write::{}'.format(resource_id))
    if resource_id is not None:
        if self.driver._es.exists(index=self.driver._index, id=resource_id, doc_type='_doc'):
            raise ValueError('Resource "{}" already exists, use update instead'.format(resource_id))
    return self.driver._es.index(index=self.driver._index, id=resource_id, body=obj, doc_type='_doc', refresh='wait_for')['_id']