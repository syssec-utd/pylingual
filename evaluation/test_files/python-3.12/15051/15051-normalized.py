def product_line_items(request, form):
    """ Shows each product line item from invoices, including their date and
    purchashing customer. """
    products = form.cleaned_data['product']
    categories = form.cleaned_data['category']
    invoices = commerce.Invoice.objects.filter(Q(lineitem__product__in=products) | Q(lineitem__product__category__in=categories), status=commerce.Invoice.STATUS_PAID).select_related('cart', 'user', 'user__attendee', 'user__attendee__attendeeprofilebase').order_by('issue_time')
    headings = ['Invoice', 'Invoice Date', 'Attendee', 'Qty', 'Product', 'Status']
    data = []
    for invoice in invoices:
        for item in invoice.cart.productitem_set.all():
            if item.product in products or item.product.category in categories:
                output = []
                output.append(invoice.id)
                output.append(invoice.issue_time.strftime('%Y-%m-%d %H:%M:%S'))
                output.append(invoice.user.attendee.attendeeprofilebase.attendee_name())
                output.append(item.quantity)
                output.append(item.product)
                cart = invoice.cart
                if cart.status == commerce.Cart.STATUS_PAID:
                    output.append('PAID')
                elif cart.status == commerce.Cart.STATUS_ACTIVE:
                    output.append('UNPAID')
                elif cart.status == commerce.Cart.STATUS_RELEASED:
                    output.append('REFUNDED')
                data.append(output)
    return ListReport('Line Items', headings, data)