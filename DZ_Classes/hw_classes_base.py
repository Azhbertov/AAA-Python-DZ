from math import log


TRAIN_CORPUS = [
    'Марс сигнал сигнал',
    'Марс пыль',
    'Марс сигнал антенна',
]

CHECK_CORPUS = [
    'СИГНАЛ шум сигнал',
    'антенна пыль',
    'марс марс марс',
    'комета',
    '',
]


class CountVectorizer:
    def __init__(self, lowercase=True, ngram_size=1):
        self.lowercase = lowercase
        self.ngram_size = ngram_size
        self._vocabulary = {}

    def add_word(self, word):
        if word not in self._vocabulary:
            self._vocabulary[word] = len(self._vocabulary)
        return self._vocabulary[word]

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()
        words = text.split()
        if self.ngram_size == 1:
            return words
        elif len(words) < 2:
            return []
        else:
            result = []
            for i in range(len(words) - 1):
                result.append(f'{words[i]} {words[i + 1]}')
            return result

    def fit(self, corpus):
        not_empty_texts = 0
        for text in corpus:
            if self.tokenize(text):
                not_empty_texts += 1
        if not_empty_texts == 0:
            raise ValueError('В новом корпусе нет токенов')
        else:
            self._vocabulary = {}
            for text in corpus:
                for word in self.tokenize(text):
                    self.add_word(word)
            return self

    def transform(self, corpus):
        if self._vocabulary:
            result = []
            for text in corpus:
                frequencies = [0] * len(self._vocabulary)
                for word in self.tokenize(text):
                    if word in self._vocabulary:
                        index = self._vocabulary[word]
                        frequencies[index] += 1
                result.append(frequencies)
            return result
        else:
            raise RuntimeError('Сначала нужно запустить fit')

    def get_feature_names(self):
        return [
            word
            for word, index in sorted(
                self._vocabulary.items(),
                key=lambda val: val[1],
            )
        ]

    def fit_transform(self, corpus):
        return self.fit(corpus).transform(corpus)

    @property
    def vocabulary(self):
        return self._vocabulary

    @vocabulary.setter
    def vocabulary(self, new_vocabulary):
        self._vocabulary = new_vocabulary

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = {}

    def to_dict(self):
        return {
            'lowercase': self.lowercase,
            'ngram_size': self.ngram_size,
            'vocabulary': self._vocabulary.copy()
        }

    @classmethod
    def from_dict(cls, state):
        copy = cls(state['lowercase'], state['ngram_size'])
        copy.vocabulary = state['vocabulary'].copy()
        return copy


class BinaryVectorizer(CountVectorizer):
    def transform(self, corpus):
        result = []
        for frequencies in super().transform(corpus):
            existences = [0] * len(self._vocabulary)
            for index in range(len(frequencies)):
                if frequencies[index] > 0:
                    existences[index] = 1
            result.append(existences)
        return result


class TfidfVectorizer(CountVectorizer):
    def __init__(self, lowercase=True, ngram_size=1, use_idf=True):
        super().__init__(lowercase, ngram_size)
        self._idf = []
        self.use_idf = use_idf

    def fit(self, corpus):
        super().fit(corpus)
        self._idf = []
        if self.use_idf:
            N = len(corpus)
            for word in super().get_feature_names():
                cnt = 0
                for text in corpus:
                    if word in self.tokenize(text):
                        cnt += 1
                self._idf.append(log((N + 1) / (cnt + 1)) + 1)
        return self

    def transform(self, corpus):
        result = []
        voc_len = len(self._vocabulary)
        for frequencies in super().transform(corpus):
            L = sum(frequencies)
            if L != 0:
                tf = [f / L for f in frequencies]
                if self.use_idf:
                    tfidf = [0] * voc_len
                    for index in range(len(tf)):
                        tfidf[index] = tf[index] * self._idf[index]
                    result.append(tfidf)
                else:
                    result.append(tf)
            else:
                result.append([0] * voc_len)
        return result

    @classmethod
    def from_config(cls, config):
        return cls(
            lowercase=config.get('lowercase', True),
            use_idf=config.get('use_idf', True),
        )

    @property
    def idf(self):
        return self._idf.copy()


class KeywordExtractor:
    def __init__(self, v, top_n=3):
        self.top_n = top_n
        self.vectorizer = v

    def fit(self, corpus):
        self.vectorizer.fit(corpus)
        return self

    def extract(self, corpus):
        result = []
        words = self.vectorizer.get_feature_names()
        all_weights = self.vectorizer.transform(corpus)
        for weights in all_weights:
            pairs = []
            for word, weight in zip(words, weights):
                if weight > 0:
                    pairs.append((word, weight))
            pairs.sort(key=lambda pairs: (-pairs[1], pairs[0]))
            result.append(pairs[:self._top_n])
        return result

    @property
    def top_n(self):
        return self._top_n

    @top_n.setter
    def top_n(self, top_n):
        if type(top_n) is not int or top_n < 1:
            raise ValueError('top_n должно быть целым положительным числом')
        self._top_n = top_n


def demo():
    print('1. Веса TF-IDF')
    tfidf = TfidfVectorizer.from_config({})
    matrix = tfidf.fit_transform(TRAIN_CORPUS)
    print('Слова:', tfidf.get_feature_names())
    print('IDF:', tfidf.idf)
    print('Первая матрица:', matrix)  # обучение
    print('Вторая матрица:', tfidf.transform(CHECK_CORPUS))  # тест
    idf = tfidf.idf
    idf.clear()
    print('IDF после очистки:', tfidf.idf)  # очистка копии

    print('\n2. Настройки и новый fit')
    tf = TfidfVectorizer.from_config({'lowercase': False, 'use_idf': False})
    corpus = ['Марс марс', 'МАРС сигнал']
    matrix = tf.fit_transform(corpus)
    print('Слова:', tf.get_feature_names())
    print('IDF:', tf.idf)
    print('TF:', matrix)
    tfidf.fit(['Венера облака'])
    print('Слова:', tfidf.get_feature_names())
    print('IDF:', tfidf.idf)
    print('Матрица:', tfidf.transform(['Марс Венера облака']))

    print('\n3. Ключевые слова')
    e = KeywordExtractor(tfidf, top_n=2)
    e.fit(TRAIN_CORPUS)
    print('top_n = 2:', e.extract(CHECK_CORPUS))
    e.top_n = 1
    print('top_n = 1:', e.extract(CHECK_CORPUS))
    try:
        e.top_n = 0
    except ValueError as error:
        print('Ошибка:', error)


if __name__ == '__main__':
    demo()
