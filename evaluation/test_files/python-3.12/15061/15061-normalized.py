def available_credit(context):
    """ Calculates the sum of unclaimed credit from this user's credit notes.

    Returns:
        Decimal: the sum of the values of unclaimed credit notes for the
            current user.

    """
    notes = commerce.CreditNote.unclaimed().filter(invoice__user=user_for_context(context))
    ret = notes.values('amount').aggregate(Sum('amount'))['amount__sum'] or 0
    return 0 - ret