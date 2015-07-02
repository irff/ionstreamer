from flask import Blueprint, render_template, request
from threading import Thread, current_thread

import sqlite3, json, time, datetime


stream = Blueprint('stream', __name__, template_folder='application/templates')


@stream.route('/stream', methods=['POST'])
def _stream():
  db_session = sqlite3.connect('ionstreamer.db')
  c = db_session.cursor()
  c.execute('insert or ignore into streamings values(?)', (request.form['keyword'],))
  db_session.commit()
  db_session.close()
  return "stream "+request.form['keyword']+" ok\n"





@stream.route('/unstream', methods=['POST'])
def _unstream():
  db_session = sqlite3.connect('ionstreamer.db')
  c = db_session.cursor()
  if request.form['keyword']:
    c.execute('delete from streamings where keyword=?', (request.form['keyword'],))
  else:
    c.execute('delete from streamings')
  db_session.commit()
  db_session.close()
  return "unstream "+request.form['keyword']+" ok\n"





@stream.route('/streamings', methods=['GET'])
def streamings():
  return json.dumps(_streamings())

def _streamings():
  db_session = sqlite3.connect('ionstreamer.db')
  c = db_session.cursor()
  res = c.execute('select * from streamings').fetchall()
  db_session.commit()
  db_session.close()
  return map(lambda (x,): x, res)





@stream.route('/results/<keyword>', methods=['GET'])
def results(keyword):
  ret = ""
  for r in _results(keyword, 1000111):
    ret += json.dumps(r) + "\n"
  return ret






#####################################################
# these blocks will be replaced using elasticsearch #
#####################################################
# def _results(keyword,limit):
#   db_session = sqlite3.connect('ionstreamer.db')
#   c = db_session.cursor()
#   res = c.execute('select * from results where keyword=? order by id desc limit ?', (keyword,limit)).fetchall()
#   res = map(lambda (x,y,z): z, res)
#   db_session.commit()
#   db_session.close()
#   return res

# def _insert_to_results(data):
#   db_session = sqlite3.connect('ionstreamer.db')
#   c = db_session.cursor()
#   c.executemany('insert or ignore into results (keyword, result) values(?, ?)', data)
#   db_session.commit()
#   db_session.close()

from elasticsearch import Elasticsearch, helpers
es = Elasticsearch()

def _results(keyword, limit):
  try:
    res = es.search(index='ionstreamer-tw', doc_type=keyword, sort='_id:desc', size=limit)
    return map(lambda x: x['_source'], res['hits']['hits'])
  except Exception, e:
    return []

def _save(keyword, data):
  for d in data:
    es.index(index='ionstreamer-tw', doc_type=keyword, id=datetime.datetime.now(), body=d)
  # data = map(lambda x: {
  #   '_index': 'ionstreamer-tw',
  #   '_type': keyword,
  #   '_id': '%.6lf'%time.time(),
  #   '_source': x
  #   }, data)
  # for d in data: print json.dumps(d)[:70]
  # print '--'*40
  # time.sleep(3)
  # print helpers.bulk(es, data)

#####################################################
# these blocks will be replaced using elasticsearch #
#####################################################




# run the twitter streamer
import twitter
CONSUMER_KEY = 'QggSVBP9t2RR4yzIvJpLHxHrL'
CONSUMER_SECRET ='ncRsiSeemxz02pEUMSRhVuEtKlWxFOyCPvCNwwWKL1cZQLY2TN'
OAUTH_TOKEN = '165650047-sNAi13v3VdDk8nhqMLmcdgTVzkR2Ton749BIntQ7'
OAUTH_TOKEN_SECRET = 'OM5JGhgswebcx8WYxn8yGrwPQdexb5VS00UIoguD117VU'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

def search_twit(keyword):
  print "executing %s" %  current_thread()
  try:
    res = twitter_api.search.tweets(q=keyword, count=100)['statuses']
  except Exception, e:
    print e
    res = []

  res = map(lambda x:{
    'text': x['text'],
    'created_at': x['created_at'],
    'username': x['user']['screen_name'],
    'name': x['user']['name'],
    'image': x['user']['profile_image_url'],
    # 'place': x['place']['full_name'],
    # 'coordinate': x['coordinates']['coordinates']
    }, res)


  prev_res = map(lambda x: (x['username'], x['text']), _results(keyword,limit=100))
  res = filter(lambda x: (x['username'], x['text']) not in prev_res, res)

  _save(keyword, res)
  
  print "+%d" % len(res)
  print "-----------------------------------------------------------"


def stream_twit():
  import os
  nomor = 1
  while True:
    if os.path.exists('dead'): break
    for keyword in _streamings():
      Thread(target=search_twit, name="search_twit "+keyword+' '+str(nomor), args=(keyword,)).start()
      nomor += 1
    time.sleep(5) # actually 20


Thread(target=stream_twit, name="stream_twit").start()
