def manual_payment(request, invoice_id):
    """ Allows staff to make manual payments or refunds on an invoice.

    This form requires a login, and the logged in user needs to be staff.

    Arguments:
        invoice_id (castable to int): The invoice ID to be paid

    Returns:
        render:
            Renders ``registrasion/manual_payment.html`` with the following
            data::

                {
                    "invoice": models.commerce.Invoice(),
                    "form": form,   # A form that saves a ``ManualPayment``
                                    # object.
                }

    """
    FORM_PREFIX = 'manual_payment'
    current_invoice = InvoiceController.for_id_or_404(invoice_id)
    form = forms.ManualPaymentForm(request.POST or None, prefix=FORM_PREFIX)
    if request.POST and form.is_valid():
        form.instance.invoice = current_invoice.invoice
        form.instance.entered_by = request.user
        form.save()
        current_invoice.update_status()
        form = forms.ManualPaymentForm(prefix=FORM_PREFIX)
    data = {'invoice': current_invoice.invoice, 'form': form}
    return render(request, 'registrasion/manual_payment.html', data)