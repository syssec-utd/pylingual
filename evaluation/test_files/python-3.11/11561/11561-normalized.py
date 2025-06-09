def case(institute_id, case_name):
    """Display one case."""
    institute_obj, case_obj = institute_and_case(store, institute_id, case_name)
    data = controllers.case(store, institute_obj, case_obj)
    return dict(institute=institute_obj, case=case_obj, **data)