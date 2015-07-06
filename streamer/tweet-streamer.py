from os.path import abspath
import sys
sys.path.append(abspath(''))

from tokenmanager import gettoken
import database.dbkeyword as dbk
import database.dbresult as dbr

from time import sleep
from datetime import timedelta
from dateutil.parser import parse

from TwitterSearch import TwitterSearchOrder, TwitterSearch


def get_tso(keyword):
    tso = TwitterSearchOrder()
    for k in keyword.split():
      if k[0] == '@':
        tso.add_keyword(['from:'+k[1:], 'to:'+k[1:]], or_operator = True)
      else:
        tso.add_keyword([k])
    # print tso.create_search_url()
    return tso

def get_tso_up(row):
  tso = get_tso(row.keyword)
  if row.max_id > 0: tso.set_since_id(row.max_id)
  return tso

def get_tso_down(row):
  tso = get_tso(row.keyword)
  if row.since_id > 0: tso.set_max_id(row.since_id-1)
  return tso

def gather(row):
  try:
    dbk.set( {'keyword': row.keyword, 'processing': 1} )

    # searching up
    tsoup = get_tso_up(row)
    token = gettoken()
    try:
      ts = TwitterSearch(token.CONSUMER_KEY, token.CONSUMER_SECRET, token.OAUTH_TOKEN, token.OAUTH_TOKEN_SECRET, verify = False)
      tweets = ts.search_tweets(tsoup)['content']['statuses']
      
      for t in tweets:
        t['created_at'] = parse( t['created_at'] )
        dbr.set(row.keyword, t)
      
      if len(tweets):
        dbk.set( {'keyword': row.keyword, 'max_id': tweets[0]['id']} )

      print "[UP] %s: +%d" % (row.keyword, len(tweets))
 
    except Exception as e:
      print "%s: %s" % (token.name, str(e))


    if row.since_id > -1:
      #searching down
      tsodown = get_tso_down(row)
      token = gettoken()
      try:
        ts = TwitterSearch(token.CONSUMER_KEY, token.CONSUMER_SECRET, token.OAUTH_TOKEN, token.OAUTH_TOKEN_SECRET, verify = False)
        tweets = ts.search_tweets(tsodown)['content']['statuses']

        for t in tweets:
          t['created_at'] = parse( t['created_at'] )
          dbr.set(row.keyword, t)

        if len(tweets):
          dbk.set( {'keyword': row.keyword, 'since_id': tweets[-1]['id']} )
        else:
          dbk.set( {'keyword': row.keyword, 'since_id': -1} )

        print "[DOWN] %s: +%d" % (row.keyword, len(tweets))

      except Exception as e:
        print "%s: %s" % (token.name, str(e))
        tweets = []
  except Exception as e:
    print e
  finally:
    dbk.set( {'keyword': row.keyword, 'processing': 0} )


while True:
  for k in [x for x in dbk.get() if x.status == 'active' and x.processing == 0]:
    if k.keyword in {x.keyword for x in dbk.get() if x.status == 'active' and x.processing == 0}:
      gather(k)
  sleep(5)
