from flask import Blueprint, render_template, request

import sqlite3, json


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
  return res







@stream.route('/results', methods=['GET'])
def results():
  return json.dumps(_results())

def _results(keyword=None):
  db_session = sqlite3.connect('ionstreamer.db')
  c = db_session.cursor()
  if True or keyword == None:
    res = c.execute('select * from results').fetchall()
  else:
    res = c.execute('select * from results where keyword=?', (keyword,)).fetchall()
  db_session.commit()
  db_session.close()
  return res


def _insert_to_results(keyword, r):
  db_session = sqlite3.connect('ionstreamer.db')
  c = db_session.cursor()
  c.execute('insert or ignore into results values(?, ?)', (keyword, r))
  db_session.commit()
  db_session.close()




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
  res = twitter_api.search.tweets(q=keyword, count=100)['statuses']
  res = map(lambda x:{'id': x['id'], 'text': x['text'], 'created_at': x['created_at']}, res)
  prev_res = _results(keyword)
  # res = filter(lambda x: x not in prev_res, res)
  # for r in res: _insert_to_results(keyword, r)
  for r in prev_res: print r


def stream_twit():
  db_session = sqlite3.connect('ionstreamer.db')
  c = db_session.cursor()

  import os, time
  while True:
    if os.path.exists('dead'): break
    for keyword in _streamings():
      Thread(target=search_twit, name="search_twit", args=[keyword]).start()
    time.sleep(5) # actually 20
  db_session.close()


from threading import Thread
Thread(target=stream_twit, name="stream_twit").start()
