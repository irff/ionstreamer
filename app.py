from flask import Flask
app = Flask(__name__)

import threading
import time
import sqlite3
import json

import twitter

# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information 
# on Twitter's OAuth implementation.

CONSUMER_KEY = 'QggSVBP9t2RR4yzIvJpLHxHrL'
CONSUMER_SECRET ='ncRsiSeemxz02pEUMSRhVuEtKlWxFOyCPvCNwwWKL1cZQLY2TN'
OAUTH_TOKEN = '165650047-sNAi13v3VdDk8nhqMLmcdgTVzkR2Ton749BIntQ7'
OAUTH_TOKEN_SECRET = 'OM5JGhgswebcx8WYxn8yGrwPQdexb5VS00UIoguD117VU'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# Nothing to see by displaying twitter_api except that it's now a
# defined variable


# database
main_db = sqlite3.connect('tmp.db')
# main_db.execute('insert or ignore into result (keyword, result) values("alfan", "alfan is on twitter")')
# main_db.commit()
# print main_db.execute('select * from result').fetchall()
# q = "DROP TABLE IF EXISTS `result`; CREATE TABLE `result` (`id` INTEGER NOT NULL, `keyword` varchar(256) NOT NULL, `result` text NOT NULL, PRIMARY KEY (`id`) ); DROP TABLE IF EXISTS `streaming`; CREATE TABLE `streaming` (`keyword` varchar(256) NOT NULL, PRIMARY KEY (`keyword`) );"
# for qq in q.split(";"):
#   main_db.execute(qq)
# main_db.commit()
# exit()

def enq_table(table, data, db=main_db):
  if table == 'streaming':
    db.execute('insert or ignore into streaming values(?)', (data,))
  else:
    db.executemany('insert or ignore into result (keyword, result) values(?, ?)', data)
  db.commit()
  
def get_table(table, keyword='', db=main_db):
  if len(keyword) == 0:
    return db.execute("select * from "+table).fetchall()
  else:
    return db.execute("select * from "+table+" where keyword=?", (keyword,)).fetchall()

def remove_table(table, keyword='', db=main_db):
  if len(keyword) == 0:
    db.execute("delete from "+table)
  else:
    db.execute("delete from "+table+" where keyword=?", (keyword,))
  db.commit()


def search_twit(keyword):
  time.sleep(1)
  print "streaming %s is running.." % keyword
  this_db = sqlite3.connect('tmp.db')
  prev_res = []
  while True:
    if len(get_table('streaming', keyword, db=this_db)) < 1: break
    res = twitter_api.search.tweets(q=keyword, count=2)['statuses']
    res = map(lambda x: x['text'], res)
    res = filter(lambda x: x not in prev_res, res)
    prev_res = prev_res+res
    enq_table('result', map(lambda x: (keyword, x), res), db=this_db)
    time.sleep(3)


@app.route('/')
def hello_world():
  res = twitter_api.search.tweets(q='alfan', count=100)['statuses']
  ret = ''
  for x in res:
    ret += json.dumps(x['text'])+'\n'
  return ret

@app.route('/stream/<keyword>')
def stream(keyword):
  enq_table('streaming', keyword)
  threading.Thread(target=search_twit, name="th_"+keyword, args=[keyword]).start()
  return "streaming %s enqueued!" % keyword

@app.route('/unstream/<keyword>')
def unstream(keyword=''):
  remove_table('streaming', keyword)
  return "streaming %s removed!" % keyword

@app.route('/streamings')
def streamings():
  return json.dumps(get_table('streaming'))

@app.route('/getresult/<keyword>')
def getresult(keyword):
  return json.dumps(get_table('result', keyword))

@app.route('/removeresult/<keyword>')
def removeresult(keyword=''):
  remove_table('result', keyword)
  return "result %s removed!" % keyword

@app.route('/results')
def results():
  return json.dumps(get_table('result'))

# RUN ALL
for q in get_table('streaming'):
  stream(list(q)[0])
# print unstream()

if __name__ == '__main__':
  app.run()
