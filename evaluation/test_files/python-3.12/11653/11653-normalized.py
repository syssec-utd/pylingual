def update_case(self, case_obj):
    """Update a case in the database

        The following will be updated:
            - collaborators: If new collaborators these will be added to the old ones
            - analysis_date: Is updated to the new date
            - analyses: The new analysis date will be added to old runs
            - individuals: There could be new individuals
            - updated_at: When the case was updated in the database
            - rerun_requested: Is set to False since that is probably what happened
            - panels: The new gene panels are added
            - genome_build: If there is a new genome build
            - genome_version: - || -
            - rank_model_version: If there is a new rank model
            - madeline_info: If there is a new pedigree
            - vcf_files: paths to the new files
            - has_svvariants: If there are new svvariants
            - has_strvariants: If there are new strvariants
            - multiqc: If there's an updated multiqc report location
            - mme_submission: If case was submitted to MatchMaker Exchange

            Args:
                case_obj(dict): The new case information

            Returns:
                updated_case(dict): The updated case information
        """
    LOG.info('Updating case {0}'.format(case_obj['_id']))
    old_case = self.case_collection.find_one({'_id': case_obj['_id']})
    updated_case = self.case_collection.find_one_and_update({'_id': case_obj['_id']}, {'$addToSet': {'collaborators': {'$each': case_obj['collaborators']}, 'analyses': {'date': old_case['analysis_date'], 'delivery_report': old_case.get('delivery_report')}}, '$set': {'analysis_date': case_obj['analysis_date'], 'delivery_report': case_obj.get('delivery_report'), 'individuals': case_obj['individuals'], 'updated_at': datetime.datetime.now(), 'rerun_requested': False, 'panels': case_obj.get('panels', []), 'genome_build': case_obj.get('genome_build', '37'), 'genome_version': case_obj.get('genome_version'), 'rank_model_version': case_obj.get('rank_model_version'), 'madeline_info': case_obj.get('madeline_info'), 'vcf_files': case_obj.get('vcf_files'), 'has_svvariants': case_obj.get('has_svvariants'), 'has_strvariants': case_obj.get('has_strvariants'), 'is_research': case_obj.get('is_research', False), 'research_requested': case_obj.get('research_requested', False), 'multiqc': case_obj.get('multiqc'), 'mme_submission': case_obj.get('mme_submission')}}, return_document=pymongo.ReturnDocument.AFTER)
    LOG.info('Case updated')
    return updated_case