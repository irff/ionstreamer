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
  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'date_histogram', field='created_at', interval='hour')
  buckets = s.execute().aggregations.freq.buckets

  from random import randint
  return map(lambda b: (b.key,b.doc_count,randint(0,b.doc_count/2),randint(0,b.doc_count/2)), buckets)

def get_top_mention(keyword):
  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='entities.user_mentions.screen_name', size = 5)
  buckets = s.execute().aggregations.freq.buckets
  return map(lambda b: ('@'+b.key, b.doc_count), buckets)

def get_top_posting(keyword):
  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='user.screen_name', size = 5)
  buckets = s.execute().aggregations.freq.buckets
  return map(lambda b: ('@'+b.key, b.doc_count), buckets)


def get_top_retweet(keyword):
  st = time.time()
  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='retweeted_status.id_str', size = 1000111000, collect_mode = "breadth_first")
  buckets = s.execute().aggregations.freq.buckets
  print len(buckets)
  counted = map(lambda b: dbr.get_search_instance(keyword).query('multi_match', query = b.key, fields = ['id_str','retweeted_status.id_str']).execute().hits[0].to_dict(), buckets)
  counted.sort(lambda x, y: cmp(y['retweet_count'], x['retweet_count']))
  print time.time() - st
  return counted[:5]