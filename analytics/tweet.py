from os.path import abspath
import sys
sys.path.append(abspath(''))

from datetime import timedelta
from dateutil.parser import parse
import database.dbresult as dbr

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
  data = dbr.get_fields(keyword, fields="created_at", size = 1000111000)
  data = map(lambda x: (parse(x['created_at'][0]) + timedelta(hours = 7)).strftime("%Y-%m-%d %H:00:00"), data)
  data.sort()
  ret = []
  for d in data:
    if ret == [] or ret[-1][0] != d:
      ret.append([d,1])
    else:
      ret[-1][1] += 1
  return ret