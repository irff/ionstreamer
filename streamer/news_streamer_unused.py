from os.path import abspath, isfile
import sys
sys.path.append(abspath(''))

from config import ESHOST_NEWS
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import database.dbtoken as dbt
import database.dbkeyword as dbk
import database.dbresultnews as dbr

from time import sleep, time

import urllib3
urllib3.disable_warnings()

def gather(row):
  dbk.setData( {'keyword': row.keyword, 'processing': 1} )
  try:
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
    
    print "[UP] %s: +%d" % (row.keyword, len(r))

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

    print "[DOWN] %s: +%d" % (row.keyword, len(r))

  finally:
    dbk.setData( {'keyword': row.keyword, 'processing': 0} )


from config import INDEX
from base64 import b64encode

def run_streamer():
  while True:
    try:
      row = dbk.getOne()
      if row != None: gather(row)
      sleep(1)
    except Exception as e:
      print >> sys.stderr, "exception: %s" % str(e)
      with open('/tmp/news_streamer_log', 'a+') as fileerr: print >> fileerr, "exception: %s" % str(e)

      while True:
        try:
          dbk.reset()
          break
        except Exception as e:
          print >> sys.stderr, str(e)
          sleep(10)


run_streamer()
