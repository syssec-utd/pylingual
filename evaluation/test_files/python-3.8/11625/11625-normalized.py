def load_variant_bulk(self, variants):
    """Load a bulk of variants

        Args:
            variants(iterable(scout.models.Variant))

        Returns:
            object_ids
        """
    if not len(variants) > 0:
        return
    LOG.debug('Loading variant bulk')
    try:
        result = self.variant_collection.insert_many(variants)
    except (DuplicateKeyError, BulkWriteError) as err:
        for var_obj in variants:
            try:
                self.upsert_variant(var_obj)
            except IntegrityError as err:
                pass
    return