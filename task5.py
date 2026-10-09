from collections import defaultdict


def reviews_analyze(reviews_list):
    reviews_dict = defaultdict(list)
    for review in reviews_list:
        reviews_dict[review['product'].capitalize()].append(
            review['stars']
        )

    mean_evaluation = {
        product: sum(stars) / len(stars)
        for product, stars in reviews_dict.items()
    }
    more_2_reviews = {
        product: evaluation
        for product, evaluation in mean_evaluation.items()
        if len(reviews_dict[product]) >= 2
    }
    worst_product = min(more_2_reviews, key=more_2_reviews.get)
    low_evaluation_reviews = len([
        review['id']
        for review in reviews_list
        if review['stars'] == 1 or review['stars'] == 2
    ])

    print(f'Средняя оценка каждого товара: {mean_evaluation}')
    print('Худший товар по средней оценке среди тех, у кого 'f'хотя бы два отзыва: {worst_product}')
    print(f'Сколько отзывов на 1 или 2 звезды: {low_evaluation_reviews}')
    print('Какую долю всех отзывов они составляют: 'f'{low_evaluation_reviews / len(reviews_list)}')


if __name__ == '__main__':
    reviews = [
        {'id': 1, 'product': 'Чехол', 'stars': 5},
        {'id': 1, 'product': 'Чехол', 'stars': 3},
        {'id': 1, 'product': 'Чехол', 'stars': 4},
        {'id': 2, 'product': 'Наушники', 'stars': 2},
        {'id': 2, 'product': 'наушники', 'stars': 2},
        {'id': 2, 'product': 'НАУШНИКИ', 'stars': 5},
        {'id': 3, 'product': 'Планшет', 'stars': 5},
        {'id': 4, 'product': 'Колонка', 'stars': 4},
        {'id': 4, 'product': 'Колонка', 'stars': 4},
        {'id': 5, 'product': 'Кабель', 'stars': 1},
    ]
    reviews_analyze(reviews)
