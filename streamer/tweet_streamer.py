from os.path import abspath, isfile
import sys
sys.path.append(abspath(''))

import database.dbtoken as dbt
import database.dbkeyword as dbk
import database.dbresult as dbr

from time import sleep, time
from dateutil.parser import parse
from shlex import split

from TwitterSearch import TwitterSearchOrder, TwitterSearch

import urllib3
urllib3.disable_warnings()

def get_tso(keyword):
    tso = TwitterSearchOrder()
    for k in split(keyword, posix = False):
      if k[0] == '"' and k[-1] == '"':
        k = k[1:-1]
      if k[0] == '@':
        tso.add_keyword(['from:'+k[1:], 'to:'+k[1:]], or_operator = True)
      else:
        tso.add_keyword([k])
    tso.set_language('id')
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
  dbk.setData( {'keyword': row.keyword, 'processing': 1} )
  try:
    # searching up
    tsoup = get_tso_up(row)
    token = dbt.getOne()
    try:
      ts = TwitterSearch(token.CONSUMER_KEY, token.CONSUMER_SECRET, token.OAUTH_TOKEN, token.OAUTH_TOKEN_SECRET, verify = False)
      tweets = ts.search_tweets(tsoup)['content']['statuses']

      for t in tweets:
        t['created_at'] = parse( t['created_at'] )
        dbr.setData(row.keyword, t)

      if len(tweets):
        dbk.setData( {'keyword': row.keyword, 'max_id': tweets[0]['id']} )

      print "[UP] %s: +%d" % (row.keyword, len(tweets))

    except Exception as e:
      print >> sys.stderr, str(e)

    if row.since_id > -1:
      #searching down
      tsodown = get_tso_down(row)
      token = dbt.getOne()
      try:
        ts = TwitterSearch(token.CONSUMER_KEY, token.CONSUMER_SECRET, token.OAUTH_TOKEN, token.OAUTH_TOKEN_SECRET, verify = False)
        tweets = ts.search_tweets(tsodown)['content']['statuses']

        for t in tweets:
          t['created_at'] = parse( t['created_at'] )
          dbr.setData(row.keyword, t)

        if len(tweets):
          dbk.setData( {'keyword': row.keyword, 'since_id': tweets[-1]['id']} )
        else:
          dbk.setData( {'keyword': row.keyword, 'since_id': -1} )

        print "[DOWN] %s: +%d" % (row.keyword, len(tweets))
        print "==="*25

      except Exception as e:
        print >> sys.stderr, str(e)


    # NEWS
    min_time = row.min_time if 'min_time' in row else '9999'
    max_time = row.max_time if 'max_time' in row else '0000'

    r = []
    # UP, gte max_time
    try:
      s = Search(using = Elasticsearch(ESHOST_NEWS, timeout = 60), index = 'langgar')
      r = s.filter('range', timestamp={"gte": max_time}).query("multi_match", query=row.keyword, fields=['title', 'content']).params(size=300, sort="timestamp:desc").execute().hits
    except Exception as e:
      print >> sys.stderr, "exception: %s" % str(e)

    row['max_time'] = r[0].timestamp if len(r) else max_time

    for news in r:
      try:
        dbr.setData(row.keyword, news.to_dict())
      except Exception as e:
        print >> sys.stderr, "exception: %s" % str(e)

    print "[NEWS UP] %s: +%d" % (row.keyword, len(r))

    r = []
    # DOWN, lte min_time
    try:
      s = Search(using = Elasticsearch(ESHOST_NEWS, timeout = 60), index = 'langgar')
      r = s.filter('range', timestamp={"lte": min_time}).query("multi_match", query=row.keyword, fields=['title', 'content']).params(size=300, sort="timestamp:desc").execute().hits
    except Exception as e:
      print >> sys.stderr, "exception: %s" % str(e)

    row['min_time'] = r[-1].timestamp if len(r) else min_time

    for news in r:
      try:
        dbr.setData(row.keyword, news.to_dict())
      except Exception as e:
        print >> sys.stderr, "exception: %s" % str(e)

    print "[NEWS DOWN] %s: +%d" % (row.keyword, len(r))

  finally:
    dbk.setData( {'keyword': row.keyword, 'processing': 0} )


from config import INDEX
from base64 import b64encode
def remove_periodically():
  HARI = 24 * 60 * 60
  for k in [x for x in dbk.getAll() if x.status == 'removed' and time() - x.last_used > 7*HARI]:
    try:
      dbr.es.indices.delete_mapping(index=INDEX, doc_type = b64encode(k.keyword), ignore = [404])
      dbk.delete(k.keyword)
      print "removed permanently: %s" % k.keyword
    except Exception as e:
      print >> sys.stderr, str(e)

def run_streamer():
  while True:
    try:
      row = dbk.getOne()
      if row != None: gather(row)
      remove_periodically()
      sleep(1)
    except Exception as e:
      print >> sys.stderr, "exception: %s" % str(e)
      with open('/tmp/tweet_streamer_log', 'a+') as fileerr: print >> fileerr, "exception: %s" % str(e)

      while True:
        try:
          dbk.reset()
          break
        except Exception as e:
          print >> sys.stderr, str(e)
          sleep(10)


run_streamer()
