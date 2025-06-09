def research(institute_id, case_name):
    """Open the research list for a case."""
    institute_obj, case_obj = institute_and_case(store, institute_id, case_name)
    user_obj = store.user(current_user.email)
    link = url_for('.case', institute_id=institute_id, case_name=case_name)
    store.open_research(institute_obj, case_obj, user_obj, link)
    return redirect(request.referrer)