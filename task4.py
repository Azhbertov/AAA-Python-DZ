def days_analyze(days_list):
    revenue_per_week = sum(day['revenue'] for day in days_list)
    max_revenue_day = max(days_list, key=lambda day: day['revenue'])['day']
    mean_revenue_per_order = {day['day']: day['revenue'] / day['orders'] for day in days_list}
    more_20_returns_days = [day['day'] for day in days_list if day['returns'] / day['orders'] > 0.2]
    print(f'Выручка за всю неделю: {revenue_per_week}')
    print(f'День с самой большой выручкой: {max_revenue_day}')
    print(f'Средняя выручка на один заказ в каждый день: {mean_revenue_per_order}')
    print(f'Дни, где возвратов больше 20% заказов: {more_20_returns_days}')


if __name__ == '__main__':
    days = [
        {"day": "пн", "orders": 20, "revenue": 40_000, "returns": 2},
        {"day": "вт", "orders": 16, "revenue": 19_200, "returns": 4},
        {"day": "ср", "orders": 25, "revenue": 55_000, "returns": 1},
        {"day": "чт", "orders": 10, "revenue": 12_000, "returns": 3},
        {"day": "пт", "orders": 30, "revenue": 48_000, "returns": 3},
    ]
    days_analyze(days)
