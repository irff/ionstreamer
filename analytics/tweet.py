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
      'count': r.hits.total,
      'status': row.status,
      'processing': row.processing,
      'tweets': ["@%s: %s"%(d.user.screen_name, d.text) for d in r.hits]
    }
  except Exception as e:
    print >> sys.stderr, "twees analytics: " + str(e)[:123]
    return {'keyword': row.keyword, 'count': 0, 'status': row.status, 'processing': row.processing, 'tweets': []}

def get_tweet_freq(keyword):
  st = time.time()

  # slice bucket into 20 pieces
  s = dbr.get_search_instance(keyword)
  awal = parse(s.params(size = 1, sort = 'id:asc').execute().hits[0].created_at)
  akhir = parse(s.params(size = 1, sort = 'id:desc').execute().hits[0].created_at)
  interval = "%ds" % ( (akhir - awal)/60 ).seconds

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('histo', 'date_histogram', field='created_at', interval=interval)
  buckets = s.execute().aggregations.histo.buckets

  from random import randint

  print "%s - top tweet freq: %lf" % (keyword, time.time() - st)
  return map(lambda b: (b.key,b.doc_count,randint(1,b.doc_count/2+1),randint(1,b.doc_count/2+1)), buckets)

def get_top_mentions(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='entities.user_mentions.screen_name', size = 7)
  buckets = s.execute().aggregations.freq.buckets

  print "%s - top mention: %lf" % (keyword, time.time() - st)
  return map(lambda b: ('@'+b.key, b.doc_count), buckets)

def get_top_postings(keyword):
  st = time.time()

  s = dbr.get_search_instance(keyword).params(size = 1000111000, search_type = 'count')
  s.aggs.bucket('freq', 'terms', field='user.screen_name', size = 7)
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

  print "%s - random tweet: %lf" % (keyword, time.time() - st)
  return map(lambda x: x.to_dict(), r.hits)

def get_tweets_at(keyword, kelas, waktu1, waktu2):
  st = time.time()

  waktu1 = parse(waktu1)
  waktu2 = parse(waktu2)
  r = dbr.get_search_instance(keyword).params(size = 10).filter('range', created_at = {'from': waktu1, 'to': waktu2}).query('function_score', random_score={}).execute()

  print "%s %s %s %s - get tweets at: %lf" % (keyword, kelas, waktu1, waktu2, time.time() - st)
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


def download_tweets_at(keyword, kelas, waktu1, waktu2):
  st = time.time()

  waktu1 = parse(waktu1)
  waktu2 = parse(waktu2)
  r = dbr.get_search_instance(keyword).params(size = 1000111000).filter('range', created_at = {'from': waktu1, 'to': waktu2}).execute()

  attributes = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
  nomor = 0

  data = [attributes]
  for t in r.hits:
    nomor += 1
    data.append([str(nomor), '@' + t.user.screen_name, '"' + t.user.name.replace('"', '""') + '"', '"' + t.text.replace('"', '""') + '"', t.created_at[:10]+' '+t.created_at[11:19], str(t.retweet_count), str(t.favorite_count)])

  print "%s %s %s %s - download tweets at: %lf" % (keyword, kelas, waktu1, waktu2, time.time() - st)
  return '\n'.join([';'.join(t) for t in data])

def download_mentions(keyword, username):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 1000111000).query('match', **{'entities.user_mentions.screen_name': username}).execute()

  attributes = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
  nomor = 0

  data = [attributes]
  for t in r.hits:
    nomor += 1
    data.append([str(nomor), '@' + t.user.screen_name, '"' + t.user.name.replace('"', '""') + '"', '"' + t.text.replace('"', '""') + '"', t.created_at[:10]+' '+t.created_at[11:19], str(t.retweet_count), str(t.favorite_count)])

  print "%s %s - download mentions: %lf" % (keyword, username, time.time() - st)
  return '\n'.join([';'.join(t) for t in data])

def download_postings(keyword, username):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 1000111000, sort='id_str:desc').query('match', **{'user.screen_name': username}).execute()

  attributes = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
  nomor = 0

  data = [attributes]
  for t in r.hits:
    nomor += 1
    data.append([str(nomor), '@' + t.user.screen_name, '"' + t.user.name.replace('"', '""') + '"', '"' + t.text.replace('"', '""') + '"', t.created_at[:10]+' '+t.created_at[11:19], str(t.retweet_count), str(t.favorite_count)])

  print "%s %s - download postings: %lf" % (keyword, username, time.time() - st)
  return '\n'.join([';'.join(t) for t in data])

def download_all(keyword):
  st = time.time()

  r = dbr.get_search_instance(keyword).params(size = 1000111, fields='user.screen_name,user.name,text,created_at,retweet_count,favorite_count', sort='id_str:desc').execute()

  attributes = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
  nomor = 0

  data = [attributes]
  for t in r.hits:
    nomor += 1
    data.append([
      str(nomor),
      '@' + t['user.screen_name'][0],
      '"' + t['user.name'][0].replace('"', '""') + '"',
      '"' + t['text'][0].replace('"', '""') + '"',
      t['created_at'][0][:10]+' '+t['created_at'][0][11:19],
      str(t['retweet_count'][0]),
      str(t['favorite_count'][0])
    ])

  print "%s - download all: %lf" % (keyword, time.time() - st)
  return '\n'.join([';'.join(t) for t in data])
