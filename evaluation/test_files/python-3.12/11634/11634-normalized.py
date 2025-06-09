def sanger_ordered(self, institute_id=None, user_id=None):
    """Get all variants with validations ever ordered.

        Args:
            institute_id(str) : The id of an institute
            user_id(str) : The id of an user

        Returns:
            sanger_ordered(list) : a list of dictionaries, each with "case_id" as keys and list of variant ids as values
        """
    query = {'$match': {'$and': [{'verb': 'sanger'}]}}
    if institute_id:
        query['$match']['$and'].append({'institute': institute_id})
    if user_id:
        query['$match']['$and'].append({'user_id': user_id})
    results = self.event_collection.aggregate([query, {'$group': {'_id': '$case', 'vars': {'$addToSet': '$variant_id'}}}])
    sanger_ordered = [item for item in results]
    return sanger_ordered