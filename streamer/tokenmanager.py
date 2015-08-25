import database.dbtoken as dbt
from datetime import datetime, timedelta
from time import time, sleep
from math import ceil

TOKEN = "token"

# def gettoken(delta = 8): # 10 tokens, 5 streamers
#   try:
#     while True:
#       tokens = [x for x in dbt.get() if ( datetime.now() - x.last_used ) > timedelta(seconds = delta)]
#       if len(tokens):
#         dbt.set( {'CONSUMER_KEY': tokens[0].CONSUMER_KEY, 'last_used': datetime.fromtimestamp( ceil(time()) ).__str__()} )
#         return tokens[0]
#       sleep(.5)
#   except Exception as e:
#     print >> sys.stderr, "tokenmanager error: %s" % str(e)
#     return None

tokens = [
  {
    'name': 'ionstreamer-1',
    'CONSUMER_KEY': 'A2HealPlVlNSjw3rRvnD8QRV7',
    'CONSUMER_SECRET': '2OlELoONajWemE5GFyCWaQJn2pSuT9wmtkNa3sxRVnOC646Tmd',
    'OAUTH_TOKEN': '165650047-zFVIH8Vk9Td1iwBa4JNzPBJhdQGiTTEvG64UnxGa',
    'OAUTH_TOKEN_SECRET': 'gDqe5PPBiBC5s8GOIH0ZQ7I4AsDxUyw2S2aP9BHyMExYp'
  },
  {
    'name': 'ionstreamer-2',
    'CONSUMER_KEY': 'fnLxpCb6OsyiQtlsRJOJqsjYv',
    'CONSUMER_SECRET': 'vwV5CqozRk7dYlHKrQxcHpedFFkR8w5gQX0Wg0NC0Wr5AQcvgW',
    'OAUTH_TOKEN': '165650047-HT1d922Xru54UUvtArQawP2h99vYLecnqR01vAtK',
    'OAUTH_TOKEN_SECRET': 'bhsIEb3cKMyuIT9v2IYFsnIpl7SEOpO8NUe3SdObWCE6e'
  },
  {
    'name': 'ionstreamer-3',
    'CONSUMER_KEY': 'IG5oRi05KtnMJ5waQMJAhAC1X',
    'CONSUMER_SECRET': '0PGIjKti23UxrpQRw4EtExBD18MWl9AuxwmXShdKOhGN2dGrOr',
    'OAUTH_TOKEN': '165650047-1r3WzaRmGh0cPnNoiIhhVuhS1DhjwQJAzZWPhlg4',
    'OAUTH_TOKEN_SECRET': 'HDDnA7ZGfBRJRCXIS77W9B7jBZn5WPnG0ejHaDLwD2Ul3'
  },
  {
    'name': 'ionstreamer-4',
    'CONSUMER_KEY': 'mlmsUwE0Im7xoAR40rdjmbd80',
    'CONSUMER_SECRET': 'BfDzWjCR9OuzUFGDqC5FxU0xsHF1JSD95rpJcD6qNOyjX4NeO4',
    'OAUTH_TOKEN': '165650047-5BAvI1wh1BZxhutSeQwjkyt5tUQ2nT3uxNqA6P7u',
    'OAUTH_TOKEN_SECRET': '54fELPoxh4o0yNb6artdR8nJsQsOsvhvyrLMPi8xQyIwc'
  },
  {
    'name': 'ionstreamer-5',
    'CONSUMER_KEY': 'phDMeAths0X5NytM5pl13sj0a',
    'CONSUMER_SECRET': 'DLpYTv2dDCvWsCWxKzKbiqGu4Ygcnq456w9TX6mEJVaHSGEcWg',
    'OAUTH_TOKEN': '165650047-RNbqgodWgqxWsUOcz95TEmXhMTi4tNxT3kglwEzv',
    'OAUTH_TOKEN_SECRET': 'PmniFgaq0t5LQ1Zy13616McqIwuxGiFGWsrx29D8SKKda'
  },
  {
    'name': 'ionstreamer-6',
    'CONSUMER_KEY': 'dmQ5ZDZVFjVgZYqJhnjHEuJbW',
    'CONSUMER_SECRET': 'fsofeAx8o14FeSjvVETSYoaL8bxuzcBchxUhA3XegMiemYZC3h',
    'OAUTH_TOKEN': '165650047-WjLwO3OHufBjeRnACG7WCP4Nt2y1HrjTZNdlJH9u',
    'OAUTH_TOKEN_SECRET': 'g4ROH7ygcRKnq5j4CfX97TDxJuKn9jB07EE5S9KGytA2N'
  },
  {
    'name': 'ionstreamer-7',
    'CONSUMER_KEY': 'p0j9vocz5fPQBkTHkGAGFFzup',
    'CONSUMER_SECRET': 'YL5noM38Z632F71xhk6gK6ik9wFE2oQj2I06hGx64yQtwEnTm1',
    'OAUTH_TOKEN': '165650047-oW1uGr0jcGJmCAoDUvAEBo8mAdUsNJLbwBCw0czi',
    'OAUTH_TOKEN_SECRET': 'FvONFtIOhssHdfgJ2fMnzxTBGSJ6f6RsrdGtEcMeil6Mz'
  },
  {
    'name': 'ionstreamer-8',
    'CONSUMER_KEY': 'RW7FP4ELLf9Ye2p7ZUv7YCxsC',
    'CONSUMER_SECRET': 'UwNgssAeZHys61Xar7L6P4nxAgXzmxrgEO261nDBWkKp3EbEnu',
    'OAUTH_TOKEN': '165650047-kqdpo6mOP08h5j6UV9uNow48EaFaW9hkhj8IOgPX',
    'OAUTH_TOKEN_SECRET': '8WCOOgClEYvgJLlGZ7Kg3aQ0rFXdbMmRPzdyKUxIlRkJG'
  },
  {
    'name': 'ionstreamer-9',
    'CONSUMER_KEY': '7arN59GQeqHT0YiY5Tg9wV94G',
    'CONSUMER_SECRET': 'tGK8CAbeeiSxjnm7mlmFXqq0HdOwHna9PKP2LYn62g48MdaW4n',
    'OAUTH_TOKEN': '165650047-YVos1Nw5LjiI24bvjS6h9ORxz8PViRdU83NNvifQ',
    'OAUTH_TOKEN_SECRET': 'pCreTqIj2ZrfBlCjPvHrjRp6HdRLvOuAGIJqz9bXyPRWr'
  },
  {
    'name': 'ionstreamer-10',
    'CONSUMER_KEY': 'ix0c8JQokq81a4VO8mNWZ0Mjf',
    'CONSUMER_SECRET': 'lPat8hh4umtyKF1pXA9TLpjPvFoohCle4ukJEDFxkuNuJMocwK',
    'OAUTH_TOKEN': '165650047-43Q5wgFH4qUWZoBUKXtMlpVG98HOwAMzpEZLkcoz',
    'OAUTH_TOKEN_SECRET': 'H1zPiywxYtiHmkfAYHvMCSgTGDHkqIIQFtuYDdildMQul'
  },
]

def gettoken(number = 0):
  return tokens[number]