from django import template


register = template.Library()

NEWS_ARTICLES = {
   'news': 'N',
   'art': 'A',
}

CENSOR_WORDS = [
    'бебебе',
    'сос',
    'сис',
    'пипка', # !!!
]

@register.filter()
def post(value, code='art'):
    postfix = NEWS_ARTICLES[code]
    return f'{value} {postfix}'


@register.filter()
def censor(value):
    """ Фильтр, который заменяет буквы нежелательных слов в заголовках и текстах статей на символ «*» """
    for word in CENSOR_WORDS:
        value = value.replace(word[1:], '*' * len(word[1:]))
    return value