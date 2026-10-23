from collections import defaultdict


def queries_analyze(queries_list):
    queries_count = len(queries_list)
    queries_dict = defaultdict(int)
    for query in queries_list:
        queries_dict[query] += 1

    most_frequent_query = max(queries_dict, key=queries_dict.get)
    share = queries_dict[most_frequent_query] / queries_count
    once_query = [
        query for query, count in queries_dict.items() if count == 1
    ]

    print(f'Сколько всего поисковых запросов в ленте: {queries_count}')
    print(f'Сколько раз ввели каждый запрос: {dict(queries_dict)}')
    print(f'Какой запрос вводили чаще всего: {most_frequent_query}')
    print(f'Какую долю всех поисков он занимает: {share}')
    print(f'Какие запросы встретились один раз: {once_query}')


if __name__ == '__main__':
    queries = [
        'чехол',
        'iphone',
        'чехол',
        'наушники',
        'iphone',
        'iphone',
        'кабель',
        'чехол',
        'iphone',
    ]
    queries_analyze(queries)
