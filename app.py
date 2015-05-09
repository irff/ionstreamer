from flask import Flask
app = Flask(__name__)

import threading
import time
import sqlite3
import json

import twitter
CONSUMER_KEY = 'QggSVBP9t2RR4yzIvJpLHxHrL'
CONSUMER_SECRET ='ncRsiSeemxz02pEUMSRhVuEtKlWxFOyCPvCNwwWKL1cZQLY2TN'
OAUTH_TOKEN = '165650047-sNAi13v3VdDk8nhqMLmcdgTVzkR2Ton749BIntQ7'
OAUTH_TOKEN_SECRET = 'OM5JGhgswebcx8WYxn8yGrwPQdexb5VS00UIoguD117VU'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


# database
main_db = sqlite3.connect('tmp.db')
# main_db.execute('insert or ignore into result (keyword, result) values("alfan", "alfan is on twitter")')
# main_db.commit()
# print main_db.execute('select * from result').fetchall()

# q = "DROP TABLE IF EXISTS `result`; CREATE TABLE `result` (`keyword` varchar(256) NOT NULL, `result` varchar(256) NOT NULL, PRIMARY KEY (`keyword`, `result`) ); DROP TABLE IF EXISTS `streaming`; CREATE TABLE `streaming` (`keyword` varchar(256) NOT NULL, PRIMARY KEY (`keyword`) );"
# for qq in q.split(";"):
#   main_db.execute(qq)
# main_db.commit()

# exit()








def enq_table(table, data, db=main_db):
  if table == 'streaming':
    db.execute('insert or ignore into streaming values(?)', (data,))
  else:
    db.executemany('insert or ignore into result values(?, ?)', data)
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









import os.path
from datetime import datetime
def search_twit(keyword):
  time.sleep(1)
  print "streaming %s is running.." % keyword
  this_db = sqlite3.connect('tmp.db')
  prev_res = datetime.min

  while (not os.path.exists('stop_all_thread')) and len(get_table('streaming', keyword, db=this_db)) > 0:
    res = twitter_api.search.tweets(q=keyword, count=100)['statuses']
    res = map(lambda x: [x['text'], datetime.strptime(x['created_at'][4:20]+x['created_at'][26:], "%b %d %H:%M:%S %Y")], res)
    res.reverse()
    top_result = res[-1][1]
    # print "=============="
    # print "just result:"
    # for x in res:
    #   print x[1], x[0][:30]

    res = filter(lambda (text, created_at): created_at > prev_res, res)
    print "%d data about %s added" % (len(res), keyword)
    # print "prev_res:", prev_res
    # print "result after filtering:"
    # for x in res:
    #   print x[1], x[0][:30]
    # print ""
    # for x in res:
    #   print x[1].strftime("%m-%b-%Y %H:%M:%S"), x[0][:40]
    ## y.strftime("%Y-%m-%d %H:%M:%S")
    res = map(lambda (text, created_at): (text, created_at.strftime("%Y-%m-%d %H:%M:%S")), res)
    enq_table('result', map(lambda x: (keyword, json.dumps(x)), res), db=this_db)
    prev_res = top_result
    time.sleep(10)
  this_db.close()
  print "streaming %s stops!" % keyword








@app.route('/')
def ganteng():
  res = twitter_api.search.tweets(q='alfan', count=100)['statuses']
  res = map(lambda x: [x['text'], datetime.strptime(x['created_at'][:20]+x['created_at'][26:], "%a %b %m %H:%M:%S %Y")], res)
  # res = map(lambda x: [x['text'], x['created_at']], res)
  for x in res:
    print x[1].strftime("%m-%b-%Y %H:%M:%S"), x[0][:40]
  return sum(map( lambda x:x+"\n", res))

@app.route('/stream/<keyword>')
def stream(keyword):
  if len(get_table('streaming', keyword)) == 0:
    enq_table('streaming', keyword)
    threading.Thread(target=search_twit, name="th_"+keyword, args=[keyword]).start()
    return "streaming %s enqueued!" % keyword
  else:
    return "%s had been enqueued before.." % keyword

@app.route('/unstream/<keyword>')
def unstream(keyword=''):
  remove_table('streaming', keyword)
  return "streaming %s removed!" % keyword

@app.route('/streamings')
def streamings():
  return json.dumps(get_table('streaming'))

@app.route('/getresult/<keyword>')
def getresult(keyword=''):
  res = get_table('result', keyword)
  return '\n'.join(map(lambda (keyword, result): keyword+": "+result, res))

@app.route('/removeresult/<keyword>')
def removeresult(keyword=''):
  remove_table('result', keyword)
  return "result %s removed!" % keyword

@app.route('/results')
def results():
  return getresult()


# RUN ALL
for q in get_table('streaming'):
  unstream(list(q)[0])
  stream(list(q)[0])
# print unstream()

if __name__ == '__main__':
  try:
    if os.path.exists('stop_all_thread'): os.remove('stop_all_thread')
    app.run()
  except Exception, e:
    pass
  finally:
    open('stop_all_thread', 'w').close()
