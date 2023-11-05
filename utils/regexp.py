import re


def review_order_list(*args, regexp=False):
    text = "Order number: {} \n Product: {}"
    pattern = r"Order number: (\d+) \n Product: (.+)"

    if regexp == False:
        order_number = args[0]
        product_name = args[1]
        return text.format(order_number, product_name)

    elif regexp == True:
        match = re.match(pattern, args[1])
        if match:
            order_id = match.group(1)
            return order_id
        return None
