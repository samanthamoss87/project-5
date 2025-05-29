def bag_contents(request):

    bag_items = []
    total = 0
    treatment_count = 0

    context = {
        'bag_items': bag_items,
        'total': total,
        'treatment_count': treatment_count
    }

    return context