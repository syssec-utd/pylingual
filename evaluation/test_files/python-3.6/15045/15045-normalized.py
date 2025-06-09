def items_sold():
    """ Summarises the items sold and discounts granted for a given set of
    products, or products from categories. """
    data = None
    headings = None
    line_items = commerce.LineItem.objects.filter(invoice__status=commerce.Invoice.STATUS_PAID).select_related('invoice')
    line_items = line_items.order_by('-price', 'description').values('price', 'description').annotate(total_quantity=Sum('quantity'))
    headings = ['Description', 'Quantity', 'Price', 'Total']
    data = []
    total_income = 0
    for line in line_items:
        cost = line['total_quantity'] * line['price']
        data.append([line['description'], line['total_quantity'], line['price'], cost])
        total_income += cost
    data.append(['(TOTAL)', '--', '--', total_income])
    return ListReport('Items sold', headings, data)