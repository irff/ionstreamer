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
    print str(e)[:123]
    return {'keyword': row.keyword, 'count': 'no results yet', 'status': row.status, 'processing': row.processing, 'tweets': []}

def get_tweet_freq(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'date_histogram', field='created_at', interval='hour')
  buckets = s.execute().aggregations.freq.buckets

  from random import randint

  print "%s - top tweet freq: %lf" % (keyword, time.time() - st)
  return map(lambda b: (b.key,b.doc_count,randint(0,b.doc_count/2),randint(0,b.doc_count/2)), buckets)

def get_top_mentions(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='entities.user_mentions.screen_name', size = 5)
  buckets = s.execute().aggregations.freq.buckets

  print "%s - top mention: %lf" % (keyword, time.time() - st)
  return map(lambda b: ('@'+b.key, b.doc_count), buckets)

def get_top_postings(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='user.screen_name', size = 5)
  buckets = s.execute().aggregations.freq.buckets

  print "%s - top posting: %lf" % (keyword, time.time() - st)
  return map(lambda b: ('@'+b.key, b.doc_count), buckets)


def get_top_retweets(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='retweeted_status.id_str', size = 3000)
  buckets = s.execute().aggregations.freq.buckets
  counted = map(lambda b: dbr.get_search_instance(keyword).params(size = 1, terminate_after = 1).query('match', **{'retweeted_status.id': b.key}).execute().hits[0].to_dict(), buckets)
  counted.sort(lambda x, y: cmp(y['retweet_count'], x['retweet_count']))

  print "%s - top retweet: %lf" % (keyword, time.time() - st)
  return counted[:10]

def get_random_tweets(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 10).execute()

  print "%s - top retweet: %lf" % (keyword, time.time() - st)
  return map(lambda x: x.to_dict(), s.hits)

def get_tweets_at(keyword, waktu):
  st = time.time()

  waktu1 = parse(waktu)
  waktu2 = parse(waktu) + timedelta(hours = 1)
  r = dbr.get_search_instance(keyword).params(size = 5).filter('range', created_at = {'from': waktu1, 'to': waktu2}).execute()

  print "%s - %s - get tweets at: %lf" % (keyword, time, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)

def get_mentions(keyword, username):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 5).query('match', **{'entities.user_mentions.screen_name': username}).execute()

  print "%s - %s - get mentions: %lf" % (keyword, username, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)

def get_postings(keyword, username):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 5).query('match', **{'user.screen_name': username}).execute()

  print "%s - %s - get postings: %lf" % (keyword, username, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)
