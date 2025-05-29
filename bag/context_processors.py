def bag_total_price(request):
    bag_items = request.session.get('bag', [])
    total_price = sum(item['price'] for item in bag_items)

    return {'total_price': total_price}