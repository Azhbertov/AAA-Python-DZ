def storage_analyze(moscow_storage, kazan_storage):
    print(f'Можно забрать в любом из двух городов: {moscow_storage & kazan_storage}')
    print(f'Есть только в Москве: {moscow_storage - kazan_storage}')
    print(f'Есть только в Казани: {kazan_storage - moscow_storage}')
    print(f'Сколько разных товаров на обоих складах вместе: {len(moscow_storage | kazan_storage)}')


if __name__ == '__main__':
    moscow = {201, 202, 203, 204}
    kazan = {203, 204, 205, 206}
    storage_analyze(moscow, kazan)
