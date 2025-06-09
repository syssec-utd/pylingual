def add_phenotype(self, institute, case, user, link, hpo_term=None, omim_term=None, is_group=False):
    """Add a new phenotype term to a case

            Create a phenotype term and event with the given information

            Args:
                institute (Institute): A Institute object
                case (Case): Case object
                user (User): A User object
                link (str): The url to be used in the event
                hpo_term (str): A hpo id
                omim_term (str): A omim id
                is_group (bool): is phenotype term a group?

        """
    hpo_results = []
    try:
        if hpo_term:
            hpo_results = [hpo_term]
        elif omim_term:
            LOG.debug('Fetching info for mim term {0}'.format(omim_term))
            disease_obj = self.disease_term(omim_term)
            if disease_obj:
                for hpo_term in disease_obj.get('hpo_terms', []):
                    hpo_results.append(hpo_term)
        else:
            raise ValueError('Must supply either hpo or omim term')
    except ValueError as e:
        raise e
    existing_terms = set((term['phenotype_id'] for term in case.get('phenotype_terms', [])))
    updated_case = case
    phenotype_terms = []
    for hpo_term in hpo_results:
        LOG.debug('Fetching info for hpo term {0}'.format(hpo_term))
        hpo_obj = self.hpo_term(hpo_term)
        if hpo_obj is None:
            raise ValueError('Hpo term: %s does not exist in database' % hpo_term)
        phenotype_id = hpo_obj['_id']
        description = hpo_obj['description']
        if phenotype_id not in existing_terms:
            phenotype_term = dict(phenotype_id=phenotype_id, feature=description)
            phenotype_terms.append(phenotype_term)
            LOG.info('Creating event for adding phenotype term for case {0}'.format(case['display_name']))
            self.create_event(institute=institute, case=case, user=user, link=link, category='case', verb='add_phenotype', subject=case['display_name'], content=phenotype_id)
        if is_group:
            updated_case = self.case_collection.find_one_and_update({'_id': case['_id']}, {'$addToSet': {'phenotype_terms': {'$each': phenotype_terms}, 'phenotype_groups': {'$each': phenotype_terms}}}, return_document=pymongo.ReturnDocument.AFTER)
        else:
            updated_case = self.case_collection.find_one_and_update({'_id': case['_id']}, {'$addToSet': {'phenotype_terms': {'$each': phenotype_terms}}}, return_document=pymongo.ReturnDocument.AFTER)
    LOG.debug('Case updated')
    return updated_case