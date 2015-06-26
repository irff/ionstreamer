from config import *
from database.dbmysql import *
import time, datetime, dateutil.parser

from TwitterSearch import TwitterSearchOrder, TwitterSearch
ts = TwitterSearch(CONSUMER_KEY[0], CONSUMER_SECRET[0], OAUTH_TOKEN[0], OAUTH_TOKEN_SECRET[0])


attributes = ['keyword', 'text', 'created_at', 'username', 'name', 'retweet_count']
before_days = datetime.timedelta(30) # 30 days


def format_created_at(s):
  t = dateutil.parser.parse(s) - datetime.timedelta(hours = 7)
  return t.strftime("%Y-%m-%d %H-%M-%S")

def gather(row):
  update(KEYWORD, {'keyword': row.keyword, 'status': 'processing'})
  try:
    tso = TwitterSearchOrder()

    [keyword, username] = row.keyword.split('@')

    if keyword != '': tso.add_keyword(keyword.split())
    if username != '': tso.add_keyword(['from:'+username, 'to:'+username], or_operator = True)
    # print tso.create_search_url()

    if row.max_id > 0: tso.set_since_id(row.max_id)

    try:
      result = ts.search_tweets(tso)

      tweets = [{'keyword': row.keyword, 'text': x['text'],
        'created_at': format_created_at(x['created_at']),
        'username': x['user']['screen_name'], 'name': x['user']['name'],
        'retweet_count': x['retweet_count']} for x in result['content']['statuses']]

    except Exception as e:
      tweets = []

    if len(tweets) > 0:
      max_id = result['content']['statuses'][0]['id']
      update(KEYWORD, {'keyword': row.keyword, 'max_id': max_id})

    tweets.reverse()

    for t in tweets:
      update(RESULT, t)

    print "%s: +%d" % (row.keyword, len(tweets))

  finally:
    update(KEYWORD, {'keyword': row.keyword, 'status': row.status})


while True:
  keywords = fetch(KEYWORD, where = {'status': 'active'})

  for k in keywords:
    keywords_now = fetch(KEYWORD, where = {'status': 'active'})

    keywords_now = {x.keyword for x in keywords_now}

    if k.keyword in keywords_now:
      gather(k)
      time.sleep(5.9)
