from config import *
from tokenmanager import *
from database.dbmysql import *
import time, datetime, dateutil.parser
import database.dbelasticsearch as dbes

from TwitterSearch import TwitterSearchOrder, TwitterSearch


def format_created_at(s):
  t = dateutil.parser.parse(s) + datetime.timedelta(hours = 7)
  return t.strftime("%Y-%m-%d %H-%M-%S")

def gather(row):
  print "gathering " + row.keyword
  since_id = row.since_id
  try:
    token = gettoken()

    ts = TwitterSearch(token.CONSUMER_KEY, token.CONSUMER_SECRET, token.OAUTH_TOKEN, token.OAUTH_TOKEN_SECRET)

    tso = TwitterSearchOrder()
    
    for k in row.keyword.split():
      if k[0] == '@':
        tso.add_keyword(['from:'+k[1:], 'to:'+k[1:]], or_operator = True)
      else:
        tso.add_keyword([k])

    def my_callback_closure(current_ts_instance): # accepts ONE argument: an instance of TwitterSearch
      queries, tweets_seen = current_ts_instance.get_statistics()
      if queries > 0 and (queries % 5) == 0: # trigger delay every 5th query
          time.sleep(60) # sleep for 60 seconds

    for tweet in ts.search_tweets_iterable(tso, callback=my_callback_closure):
      # print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
      tweet['created_at'] = format_created_at(tweet['created_at'])
      dbes.dbset(row.keyword, tweet)
      if since_id == 0 or tweet['id'] < since_id:
        since_id = tweet['id']
        dbset(KEYWORD, {'keyword': row.keyword, 'since_id': since_id})

  except Exception as e:
    print e


while True:
  keywords = dbget(KEYWORD, where = {'status': 'active'})

  for k in keywords:
    keywords_now = dbget(KEYWORD, where = {'status': 'active'})

    keywords_now = {x.keyword for x in keywords_now}

    if k.keyword in keywords_now:
      gather(k)

  time.sleep(30)