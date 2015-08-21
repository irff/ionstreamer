import sys, time
import database.dbresult as dbr

from os.path import abspath
from dateutil.parser import parse
from random import randint, random
from collections import defaultdict

sys.path.append(abspath(''))

def gettotal(keyword = None, enc = True):
  try:
    return dbr.get_search_instance(keyword, enc).params(search_type = 'count', size = 0).execute().hits.total
  except:
    return -1

def getinfo(row):
  try:
    r = dbr.get_search_instance(row.keyword).params(size = 3, sort='id_str:desc').execute()
    return {
      'keyword': row.keyword,
      'count': r.hits.total,
      'status': row.status,
      'processing': row.processing,
      'tweets': ["@%s: %s"%(d.user.screen_name, d.text) for d in r.hits]
    }
  except Exception as e:
    print >> sys.stderr, "get info: " + str(e)[:123]
    return {'keyword': row.keyword, 'count': 0, 'status': row.status, 'processing': row.processing, 'tweets': []}

def get_tweet_freq(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword)
  awal = parse(s.params(size = 1, sort = 'id_str:asc').execute().hits[0].created_at)
  akhir = parse(s.params(size = 1, sort = 'id_str:desc').execute().hits[0].created_at)
  interval = "%ds" % ( (akhir - awal)/150 ).seconds

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('histo', 'date_histogram', field='created_at', interval=interval)
  buckets = s.execute().aggregations.histo.buckets

  print "%s - top tweet freq: %lf" % (keyword, time.time() - st)
  # all tweets, positive, negative, neutral, dummy
  return map(lambda b: (b.key,b.doc_count,randint(0,b.doc_count/2),randint(0,b.doc_count/2),randint(0,b.doc_count/2),randint(0,b.doc_count/2)), buckets)

def get_top_mention(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='entities.user_mentions.screen_name', size = 10)
  buckets = s.execute().aggregations.freq.buckets

  print "%s - top mention: %lf" % (keyword, time.time() - st)
  return map(lambda b: ('@'+b.key, b.doc_count), buckets)

def get_top_posting(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='user.screen_name', size = 10)
  buckets = s.execute().aggregations.freq.buckets

  print "%s - top posting: %lf" % (keyword, time.time() - st)
  return map(lambda b: ('@'+b.key, b.doc_count), buckets)

def get_top_hashtag(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='entities.hashtags.text', size = 10)
  buckets = s.execute().aggregations.freq.buckets

  print "%s - top hashtag: %lf" % (keyword, time.time() - st)
  return map(lambda b: ('#'+b.key, b.doc_count), buckets)

def get_top_url(keyword):
  st = time.time()

  ret = defaultdict(int)

  size = 10000
  total = gettotal(keyword)
  kompresi = float(size)/total

  field = 'entities.urls.url'
  if total > size:
    r = dbr.get_search_instance(keyword).params(size = size, fields=field).query('function_score', random_score={}).execute()
  else:
    r = dbr.get_search_instance(keyword).params(size = size, fields=field).execute()

  for t in r.hits:
    if field in t:
      for u in t[field]:
        ret[u] += 1

  items = ret.items()

  print "%s - top url: %lf" % (keyword, time.time() - st)
  items.sort(key = lambda (x, y): y, reverse = True)
  return map(lambda (x,y): (x, int(y/kompresi)), items[:10]) if total > size else items[:10]

def get_top_retweets(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='retweeted_status.id_str', order = {"retweet": "desc"}, size = 10).bucket('retweet', 'min', field = 'retweet_count')
  buckets = s.execute().aggregations.freq.buckets
  counted = map(lambda b: dbr.get_search_instance(keyword).params(size = 1).query('match', **{'retweeted_status.id_str': b.key}).execute().hits[0].to_dict(), buckets)

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='id_str', order = {"retweet": "desc"}, size = 10).bucket('retweet', 'min', field = 'retweet_count')
  buckets = s.execute().aggregations.freq.buckets
  counted += map(lambda b: dbr.get_search_instance(keyword).params(size = 1).query('match', **{'id_str': b.key}).execute().hits[0].to_dict(), buckets)

  print "%s - top retweet: %lf" % (keyword, time.time() - st)
  return counted[:10]

def get_random_tweets(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 10)
  r = s.query('function_score', random_score={}).execute()

  print "%s - random tweet: %lf" % (keyword, time.time() - st)
  return map(lambda x: x.to_dict(), r.hits)

def get_tweets_at(keyword, kelas, waktu1, waktu2):
  st = time.time()

  waktu1 = parse(waktu1)
  waktu2 = parse(waktu2)
  r = dbr.get_search_instance(keyword).params(size = 10).filter('range', created_at = {'from': waktu1, 'to': waktu2}).query('function_score', random_score={}).execute()

  print "%s %s %s %s - get tweets at: %lf" % (keyword, kelas, waktu1, waktu2, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)

def get_mention(keyword, username):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 10).query('match', **{'entities.user_mentions.screen_name': username}).query('function_score', random_score={}).execute()

  print "%s - %s - get mention: %lf" % (keyword, username, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)

def get_posting(keyword, username):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 10, sort='id_str:desc').query('match', **{'user.screen_name': username}).execute()

  print "%s - %s - get posting: %lf" % (keyword, username, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)

def get_hashtag(keyword, hashtag):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 10).query('match', **{'entities.hashtags.text': hashtag[1:]}).query('function_score', random_score={}).execute()

  print "%s - %s - get hashtag: %lf" % (keyword, hashtag, time.time() - st)
  return map(lambda h: h.to_dict(), r.hits)
