def phenotypes(institute_id, case_name, phenotype_id=None):
    """Handle phenotypes."""
    institute_obj, case_obj = institute_and_case(store, institute_id, case_name)
    case_url = url_for('.case', institute_id=institute_id, case_name=case_name)
    is_group = request.args.get('is_group') == 'yes'
    user_obj = store.user(current_user.email)
    if phenotype_id:
        store.remove_phenotype(institute_obj, case_obj, user_obj, case_url, phenotype_id, is_group=is_group)
    else:
        try:
            phenotype_term = request.form['hpo_term']
            if phenotype_term.startswith('HP:') or len(phenotype_term) == 7:
                hpo_term = phenotype_term.split(' | ', 1)[0]
                store.add_phenotype(institute_obj, case_obj, user_obj, case_url, hpo_term=hpo_term, is_group=is_group)
            else:
                store.add_phenotype(institute_obj, case_obj, user_obj, case_url, omim_term=phenotype_term)
        except ValueError:
            return abort(400, 'unable to add phenotype: {}'.format(phenotype_term))
    return redirect(case_url)