def replace_many(self, mongo_collection, docs, filter_docs=None, mongo_db=None, upsert=False, collation=None, **kwargs):
    """
        Replaces many documents in a mongo collection.

        Uses bulk_write with multiple ReplaceOne operations
        https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.bulk_write

        .. note::
            If no ``filter_docs``are given, it is assumed that all
            replacement documents contain the ``_id`` field which are then
            used as filters.

        :param mongo_collection: The name of the collection to update.
        :type mongo_collection: str
        :param docs: The new documents.
        :type docs: list[dict]
        :param filter_docs: A list of queries that match the documents to replace.
            Can be omitted; then the _id fields from docs will be used.
        :type filter_docs: list[dict]
        :param mongo_db: The name of the database to use.
            Can be omitted; then the database from the connection string is used.
        :type mongo_db: str
        :param upsert: If ``True``, perform an insert if no documents
            match the filters for the replace operation.
        :type upsert: bool
        :param collation: An instance of
            :class:`~pymongo.collation.Collation`. This option is only
            supported on MongoDB 3.4 and above.
        :type collation: pymongo.collation.Collation

        """
    collection = self.get_collection(mongo_collection, mongo_db=mongo_db)
    if not filter_docs:
        filter_docs = [{'_id': doc['_id']} for doc in docs]
    requests = [ReplaceOne(filter_docs[i], docs[i], upsert=upsert, collation=collation) for i in range(len(docs))]
    return collection.bulk_write(requests, **kwargs)