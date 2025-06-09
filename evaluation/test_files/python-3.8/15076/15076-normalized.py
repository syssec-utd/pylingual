def refund(request, invoice_id):
    """ Marks an invoice as refunded and requests a credit note for the
    full amount paid against the invoice.

    This view requires a login, and the logged in user must be staff.

    Arguments:
        invoice_id (castable to int): The ID of the invoice to refund.

    Returns:
        redirect:
            Redirects to ``invoice``.

    """
    current_invoice = InvoiceController.for_id_or_404(invoice_id)
    try:
        current_invoice.refund()
        messages.success(request, 'This invoice has been refunded.')
    except ValidationError as ve:
        messages.error(request, ve)
    return redirect('invoice', invoice_id)