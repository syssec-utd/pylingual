def assign(institute_id, case_name, user_id=None):
    """Assign and unassign a user from a case."""
    (institute_obj, case_obj) = institute_and_case(store, institute_id, case_name)
    link = url_for('.case', institute_id=institute_id, case_name=case_name)
    if user_id:
        user_obj = store.user(user_id)
    else:
        user_obj = store.user(current_user.email)
    if request.form.get('action') == 'DELETE':
        store.unassign(institute_obj, case_obj, user_obj, link)
    else:
        store.assign(institute_obj, case_obj, user_obj, link)
    return redirect(request.referrer)