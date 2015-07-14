from os.path import abspath
import sys
sys.path.append(abspath(''))

from datetime import datetime, timedelta
from dateutil.parser import parse
import database.dbresult as dbr
import time
from collections import defaultdict

def getinfo(row):
  try:
    r = dbr.get_search_instance(row.keyword).params(size = 3, sort='id:desc').execute()

    return {
      'keyword': row.keyword,
      'count': '%d results'%r.hits.total,
      'status': row.status,
      'processing': row.processing,
      'tweets': ["@%s: %s"%(d.user.screen_name, d.text) for d in r.hits]
    }
  except Exception as e:
    print >> sys.stderr, "twees analytics: " + str(e)[:123]
    return {'keyword': row.keyword, 'count': 'no results yet', 'status': row.status, 'processing': row.processing, 'tweets': []}

def get_tweet_freq(keyword):
  st = time.time()

  # slice bucket into 20 pieces
  s = dbr.get_search_instance(keyword)
  awal = parse(s.params(size = 1, sort = 'id:asc').execute().hits[0].created_at)
  akhir = parse(s.params(size = 1, sort = 'id:desc').execute().hits[0].created_at)
  interval = "%ds" % ( (akhir - awal)/40 ).seconds

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('histo', 'date_histogram', field='created_at', interval=interval)
  buckets = s.execute().aggregations.histo.buckets

  from random import randint

  print "%s - top tweet freq: %lf" % (keyword, time.time() - st)
  return map(lambda b: (b.key,b.doc_count,randint(1,b.doc_count/2+1),randint(1,b.doc_count/2+1)), buckets)

def get_top_mentions(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='entities.user_mentions.screen_name', size = 10)
  buckets = s.execute().aggregations.freq.buckets

  print "%s - top mention: %lf" % (keyword, time.time() - st)
  return map(lambda b: ('@'+b.key, b.doc_count), buckets)

def get_top_postings(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='user.screen_name', size = 10)
  buckets = s.execute().aggregations.freq.buckets

  print "%s - top posting: %lf" % (keyword, time.time() - st)
  return map(lambda b: ('@'+b.key, b.doc_count), buckets)


def get_top_retweets(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='retweeted_status.id_str', order = {"retweet": "desc"}, size = 10).bucket('retweet', 'min', field = 'retweet_count')
  # s.aggs.bucket('freq', 'terms', field='retweeted_status.id_str', size = 1000111000)
  buckets = s.execute().aggregations.freq.buckets
  counted = map(lambda b: dbr.get_search_instance(keyword).params(size = 1).query('match', **{'retweeted_status.id': b.key}).execute().hits[0].to_dict(), buckets)
  # counted.sort(lambda x, y: cmp(y['retweet_count'], x['retweet_count']))

  print "%s - top retweet: %lf" % (keyword, time.time() - st)
  return counted

def get_random_tweets(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 10)
  r = s.query('function_score', random_score={}).execute()

  print "%s - top retweet: %lf" % (keyword, time.time() - st)
  return map(lambda x: x.to_dict(), r.hits)

def get_tweets_at(keyword, waktu1, waktu2):
  st = time.time()

  waktu1 = parse(waktu1)
  waktu2 = parse(waktu2)
  r = dbr.get_search_instance(keyword).params(size = 10).filter('range', created_at = {'from': waktu1, 'to': waktu2}).query('function_score', random_score={}).execute()

  print "%s - %s - get tweets at: %lf" % (keyword, time, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)

def get_mentions(keyword, username):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 10).query('match', **{'entities.user_mentions.screen_name': username}).query('function_score', random_score={}).execute()

  print "%s - %s - get mentions: %lf" % (keyword, username, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)

def get_postings(keyword, username):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 10, sort='id:desc').query('match', **{'user.screen_name': username}).execute()

  print "%s - %s - get postings: %lf" % (keyword, username, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)
