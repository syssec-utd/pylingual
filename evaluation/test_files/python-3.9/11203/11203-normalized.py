def verify(institute_id, case_name, variant_id, variant_category, order):
    """Start procedure to validate variant using other techniques."""
    (institute_obj, case_obj) = institute_and_case(store, institute_id, case_name)
    variant_obj = store.variant(variant_id)
    user_obj = store.user(current_user.email)
    comment = request.form.get('verification_comment')
    try:
        controllers.variant_verification(store=store, mail=mail, institute_obj=institute_obj, case_obj=case_obj, user_obj=user_obj, comment=comment, variant_obj=variant_obj, sender=current_app.config['MAIL_USERNAME'], variant_url=request.referrer, order=order, url_builder=url_for)
    except controllers.MissingVerificationRecipientError:
        flash('No verification recipients added to institute.', 'danger')
    return redirect(request.referrer)