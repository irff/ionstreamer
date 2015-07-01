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
  try:
    dbset(KEYWORD, {'keyword': row.keyword, 'status': 'processing'})
    tso = TwitterSearchOrder()

    for k in row.keyword.split():
      if k[0] == '@':
        tso.add_keyword(['from:'+k[1:], 'to:'+k[1:]], or_operator = True)
      else:
        tso.add_keyword([k])

    if row.max_id > 0: tso.set_since_id(row.max_id)
    # print tso.create_search_url()

    token = gettoken()
    try:
      ts = TwitterSearch(token.CONSUMER_KEY, token.CONSUMER_SECRET, token.OAUTH_TOKEN, token.OAUTH_TOKEN_SECRET, verify = False)

      result = ts.search_tweets(tso)
      tweets = result['content']['statuses']
      tweets.reverse()
    except Exception as e:
      print "%s: %s" % (token.name, str(e))
      tweets = []

    if len(tweets) > 0:
      dbset(KEYWORD, {'keyword': row.keyword, 'max_id': tweets[-1]['id']})

    for t in tweets:
      t['created_at'] = format_created_at(t['created_at'])
      dbes.dbset(row.keyword, t)

    print "%s: +%d" % (row.keyword, len(tweets))

  finally:
    dbset(KEYWORD, {'keyword': row.keyword, 'status': row.status})


while True:
  keywords = dbget(KEYWORD, where = {'status': 'active'})

  for k in keywords:
    keywords_now = dbget(KEYWORD, where = {'status': 'active'})

    keywords_now = {x.keyword for x in keywords_now}

    if k.keyword in keywords_now:
      gather(k)

  if len(keywords) < 2:
    time.sleep(5)
