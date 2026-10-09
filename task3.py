def orders_analyze(orders_list):
    returned_sum = sum(order['amount'] for order in orders_list if order['status'] == 'returned')
    returned_buyers = {order['buyer'] for order in orders_list if order['status'] == 'returned'}
    delivered_amounts = [order['amount'] for order in orders_list if order['status'] == 'delivered']
    delivered_count = len(delivered_amounts)

    print(f'На какую сумму оформили возвраты: {returned_sum}')
    print(f'Кто хотя бы раз вернул заказ: {returned_buyers}')
    print(f'Cколько заказов доставлено покупателю: {delivered_count}')
    print(f'Средний чек доставленных заказов: {sum(delivered_amounts) / delivered_count}')


if __name__ == '__main__':
    orders = [
        {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
        {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
        {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
        {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
        {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
        {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
    ]
    orders_analyze(orders)
