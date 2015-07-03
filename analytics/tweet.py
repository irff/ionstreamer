from os.path import abspath
import sys
sys.path.append(abspath(''))

from datetime import datetime, timedelta
from dateutil.parser import parse
import database.dbresult as dbr
import time
from collections import defaultdict


def getinfo(row):
  count = dbr.count(row.keyword)
  data = dbr.get(row.keyword, size = 100)
  # data = dbr.get_fields(row.keyword, fields = "created_at", size = 1000111000)
  data.sort(lambda x,y: cmp(y['created_at'],x['created_at']))

  if len(data) == 0: return {'keyword': row.keyword, 'count': 'no results yet', 'status': row.status, 'tweets': []}
  return {
    'keyword': row.keyword,
    'count': '%d results'%count,
    'status': row.status,
    'from': parse(data[-1]['created_at']).ctime(),
    'to': parse(data[0]['created_at']).ctime(),
    'tweets': ["@%s: %s"%(d['user']['screen_name'],d['text']) for d in data[:3]]
  }

def get_tweet_freq(keyword):
  st = time.time()
  data = dbr.get_fields(keyword, fields="created_at", size = 1000111000, timeout = 60)
  print time.time()-st
  
  st = time.time()
  # data = map(lambda x: (parse(x['created_at'][0]) + timedelta(hours = 7)).strftime("%Y-%m-%d %H:00:00"), data)
  #YYYY-mm-ddTHH
  seven = timedelta(hours = 7)
  data = map(lambda x:
              (datetime.strptime(x['created_at'][0][:10]+' '+x['created_at'][0][11:13], "%Y-%m-%d %H") + seven).strftime("%Y-%m-%d %H:00:00"),
              data)
  print time.time()-st

  st = time.time()
  ret = defaultdict(int)
  for d in data:
    ret[d] += 1
  print time.time()-st
  
  items = ret.items()
  items.sort()

  from random import randint
  return map(lambda (x,y): (x,y,randint(0,y/2),randint(0,y/2)), items)

def get_top_mention(keyword):
  username = "entities.user_mentions.screen_name"
  mentions = dbr.get_fields(keyword, fields=username, size = 1000111000, timeout = 60)
  freq = defaultdict(int)
  for m in mentions:
    for x in m['entities.user_mentions.screen_name']:
      freq[x] += 1
  
  items = freq.items()
  items.sort(lambda x,y: cmp(y[1], x[1]))
  return map(lambda (x,y): ('@'+x, y), items[:5])

def get_top_posting(keyword):
  username = "user.screen_name"
  usernames = dbr.get_fields(keyword, fields=username, size = 1000111000, timeout = 60)
  freq = defaultdict(int)
  for u in usernames:
    for x in u['user.screen_name']:
      freq[x] += 1
  
  items = freq.items()
  items.sort(lambda x,y: cmp(y[1], x[1]))
  return map(lambda (x,y): ('@'+x, y), items[:5])