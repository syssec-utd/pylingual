def load_exon_bulk(self, exon_objs):
    """Load a bulk of exon objects to the database

        Arguments:
            exon_objs(iterable(scout.models.hgnc_exon))

        """
    try:
        result = self.exon_collection.insert_many(transcript_objs)
    except (DuplicateKeyError, BulkWriteError) as err:
        raise IntegrityError(err)
    return result