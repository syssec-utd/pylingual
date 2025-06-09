def clinvar_objs(self, submission_id, key_id):
    """Collects a list of objects from the clinvar collection (variants of case data) as specified by the key_id in the clinvar submission

            Args:
                submission_id(str): the _id key of a clinvar submission
                key_id(str) : either 'variant_data' or 'case_data'. It's a key in a clinvar_submission object.
                              Its value is a list of ids of clinvar objects (either variants of casedata objects)

            Returns:
                clinvar_objects(list) : a list of clinvar objects (either variants of casedata)

        """
    submission = self.clinvar_submission_collection.find_one({'_id': ObjectId(submission_id)})
    if submission.get(key_id):
        clinvar_obj_ids = list(submission.get(key_id))
        clinvar_objects = self.clinvar_collection.find({'_id': {'$in': clinvar_obj_ids}})
        return list(clinvar_objects)
    else:
        return None