from config import *
from database.dbmysql import *
import time, datetime, dateutil.parser

from TwitterSearch import TwitterSearchOrder, TwitterSearch
ts = TwitterSearch(CONSUMER_KEY[1], CONSUMER_SECRET[1], OAUTH_TOKEN[1], OAUTH_TOKEN_SECRET[1])


attributes = ['keyword', 'text', 'created_at', 'username', 'name', 'retweet_count']
before_days = datetime.timedelta(30) # 30 days


def format_created_at(s):
  t = dateutil.parser.parse(s) - datetime.timedelta(hours = 7)
  return t.strftime("%Y-%m-%d %H-%M-%S")

def gather(row):
  print "gathering " + row.keyword
  since_id = row.since_id
  try:
    tso = TwitterSearchOrder()
    [keyword, username] = row.keyword.split('@')

    if keyword != '': tso.add_keyword(keyword.split())
    if username != '': tso.add_keyword(['from:'+username, 'to:'+username], or_operator = True)

    def my_callback_closure(current_ts_instance): # accepts ONE argument: an instance of TwitterSearch
      update(KEYWORD, {'keyword': row.keyword, 'since_id': since_id})
      queries, tweets_seen = current_ts_instance.get_statistics()
      if queries > 0 and (queries % 5) == 0: # trigger delay every 5th query
          time.sleep(30) # sleep for 30 seconds

    for tweet in ts.search_tweets_iterable(tso, callback=my_callback_closure):
      # print( '[%d] @%s tweeted: %s' % ( tweet['id'], tweet['user']['screen_name'], tweet['text'] ) )
      if since_id == 0 or tweet['id'] < since_id:
        since_id = tweet['id']

      tweet = {'keyword': row.keyword, 'text': tweet['text'],
      'created_at': format_created_at(tweet['created_at']),
      'username': tweet['user']['screen_name'], 'name': tweet['user']['name'],
      'retweet_count': tweet['retweet_count']}

      update(RESULT, tweet)

  except Exception as e:
    pass


while True:
  keywords = fetch(KEYWORD, where = {'status': 'active'})

  for k in keywords:
    keywords_now = fetch(KEYWORD, where = {'status': 'active'})

    keywords_now = {x.keyword for x in keywords_now}

    if k.keyword in keywords_now:
      gather(k)

  time.sleep(30)