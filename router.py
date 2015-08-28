from flask import Flask, render_template, request, Response, session, abort, redirect, flash
from flask.ext.compress import Compress
from config import DEBUG, HOST, PORT, BASE_URL
from datetime import timedelta
import database.dbkeyword as dbk
import database.dbresult as dbr
import analytics.tweet as tweeta
import analytics.download as download
import json, sys

app = Flask(__name__)
Compress(app)
app.permanent_session_lifetime = timedelta(days=1001)



def islogin():
  return session.get('username') == 'langgar'



@app.route(BASE_URL + "/")
def showhome():
  if not islogin(): return redirect(BASE_URL + '/login')
  return render_template('streamings.html', nav = 'home')


@app.route(BASE_URL + "/login", methods = ['GET'])
def showlogin(username = ''):
  if islogin():
    return redirect(BASE_URL + '/')
  else:
    return render_template('login.html', username = username)

@app.route(BASE_URL + "/login", methods = ['POST'])
def postlogin():
  try:
    username = request.form['username']
    password = request.form['password']
    session.permanent = request.form.get('remember') == 'on'

    if username == 'langgar' and password == 'hutlanggar17':
      session['username'] = request.form['username']
      return redirect(BASE_URL + '/')
    else:
      flash("username and password doesn't match")
      return showlogin(username = request.form.get('username'))
  except Exception as e:
    return abort(401)

@app.route(BASE_URL + "/logout", methods = ['GET'])
def logout():
  session.pop('username', None)
  return redirect(BASE_URL + '/login')



@app.route(BASE_URL + "/analyze/<keyword>")
def showanalyze(keyword):
  if not islogin(): return redirect(BASE_URL + '/login')
  size = tweeta.gettotal(keyword)
  return render_template('analyze-hc.html', keyword = keyword, nav = 'analyze', size = size)


@app.route(BASE_URL + "/learn", methods=['GET'])
def showlearn():
  if not islogin(): return redirect(BASE_URL + '/login')
  return render_template('learn.html', nav = 'learn')

@app.route(BASE_URL + "/learn/<keyword>", methods=['GET'])
def showlearn_keyword(keyword):
  if not islogin(): return redirect(BASE_URL + '/login')
  return render_template('learn.html', nav = 'learn', keyword = keyword)

@app.route(BASE_URL + "/learn/classified", methods=['GET'])
def showlearned():
  if not islogin(): return redirect(BASE_URL + '/login')
  size = tweeta.gettotal('LEARN', enc = False)
  return render_template('classified.html', nav = 'learn', size = size)


# LEARN
@app.route(BASE_URL + "/learn", methods=['POST'])
def learn():
  if not islogin(): return redirect(BASE_URL + '/login')
  try:
    dbr.set('LEARN', request.json, enc = False)
    return "%s classified to %s" % (request.json['id_str'], request.json['class'])
  except Exception as e:
    print >> sys.stderr, "error: " + str(e)

@app.route(BASE_URL + "/learn/randomtweets", methods=['GET'])
@app.route(BASE_URL + "/learn/randomtweets/<keyword>", methods=['GET'])
def getrandomtweets(keyword = None, count = 10):
  if not islogin(): return redirect(BASE_URL + '/login')
  if keyword:
    s = dbr.get_search_instance(keyword = keyword).params(size = count)
  else:
    s = dbr.get_search_instance().params(size = count)
  r = s.query('function_score', random_score={}).execute()
  def check_from_LEARN(tweet):
    try:
      t = dbr.get('LEARN', tweet.id_str, enc = False)
      return t['_source']
    except Exception as e:
      tweet['class'] = ''
      return tweet.to_dict()
  return json.dumps(map(check_from_LEARN, r.hits))

@app.route(BASE_URL + "/learn/classifiedtweets/<size>/<offset>", methods=['GET'])
def getclassifiedtweets(size = 10, offset = 0):
  if not islogin(): return redirect(BASE_URL + '/login')
  s = dbr.get_search_instance('LEARN', enc = False).params(size = size, from_ = offset)
  r = s.execute()
  return json.dumps(map(lambda x: x.to_dict(), r.hits))



# API
@app.route(BASE_URL + "/api/stream", methods=['POST'])
def apistream():
  if not islogin(): return abort(401)
  keyword = request.json['keyword']
  status = request.json['status']
  # if any([x.keyword == keyword and x.processing for x in dbk.get()]):
  #   return abort(503)
  return json.dumps( dbk.set(request.json) )

@app.route(BASE_URL + "/api/summary", methods=['GET'])
def summary():
  if not islogin(): return abort(401)
  keywords = [x for x in dbk.get() if x.status != 'removed']
  keywords.sort(key = lambda x: (x.status, x.keyword[1:] if x.keyword[0] in ['@', '#'] else x.keyword))
  return json.dumps( map(tweeta.getinfo, keywords) )

@app.route(BASE_URL + "/api/total/<keyword>", methods=['GET'])
def total(keyword):
  if not islogin(): return abort(401)
  return json.dumps(tweeta.gettotal(keyword))

@app.route(BASE_URL + "/api/analyze/freq/<keyword>", methods=['GET'])
def apianalyze(keyword):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_tweet_freq(keyword) )

@app.route(BASE_URL + "/api/analyze/topmention/<keyword>", methods=['GET'])
def topmention(keyword):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_top_mention(keyword) )

@app.route(BASE_URL + "/api/analyze/topposting/<keyword>", methods=['GET'])
def topposting(keyword):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_top_posting(keyword) )

@app.route(BASE_URL + "/api/analyze/tophashtag/<keyword>", methods=['GET'])
def tophashtag(keyword):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_top_hashtag(keyword) )

@app.route(BASE_URL + "/api/analyze/topretweets/<keyword>", methods=['GET'])
def topretweets(keyword):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_top_retweets(keyword) )

@app.route(BASE_URL + "/api/analyze/topurl/<keyword>", methods=['GET'])
def topurl(keyword):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_top_url(keyword) )

@app.route(BASE_URL + "/api/analyze/randomtweets/<keyword>", methods=['GET'])
def randomtweets(keyword):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_random_tweets(keyword) )

@app.route(BASE_URL + "/api/analyze/gettweetsat/<keyword>/<kelas>/<waktu1>/<waktu2>", methods=['GET'])
def gettweetsat(keyword, kelas, waktu1, waktu2):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_tweets_at(keyword, kelas, waktu1, waktu2) )

@app.route(BASE_URL + "/api/analyze/getmention/<keyword>/<username>", methods=['GET'])
def getmention(keyword, username):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_mention(keyword, username) )

@app.route(BASE_URL + "/api/analyze/getposting/<keyword>/<username>", methods=['GET'])
def getposting(keyword, username):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_posting(keyword, username) )

@app.route(BASE_URL + "/api/analyze/gethashtag/<keyword>/<hashtag>", methods=['GET'])
def gethashtag(keyword, hashtag):
  if not islogin(): return abort(401)
  return json.dumps( tweeta.get_hashtag(keyword, hashtag) )


# DOWNLOAD
@app.route(BASE_URL + "/download/tweetsat/<keyword>/<kelas>/<waktu1>/<waktu2>/<filename>", methods=['GET'])
def downloadtweetsat(keyword, kelas, waktu1, waktu2, filename):
  if not islogin(): return redirect(BASE_URL + '/login')
  return Response(download.download_tweets_at(keyword, kelas, waktu1, waktu2), mimetype='text/csv')

@app.route(BASE_URL + "/download/mention/<keyword>/<username>/<filename>", methods=['GET'])
def downloadmention(keyword, username, filename):
  if not islogin(): return redirect(BASE_URL + '/login')
  return Response(download.download_mention(keyword, username), mimetype='text/csv')

@app.route(BASE_URL + "/download/posting/<keyword>/<username>/<filename>", methods=['GET'])
def downloadposting(keyword, username, filename):
  if not islogin(): return redirect(BASE_URL + '/login')
  return Response(download.download_posting(keyword, username), mimetype='text/csv')

@app.route(BASE_URL + "/download/hashtag/<keyword>/<hashtag>/<filename>", methods=['GET'])
def downloadhashtag(keyword, hashtag, filename):
  if not islogin(): return redirect(BASE_URL + '/login')
  return Response(download.download_hashtag(keyword, hashtag), mimetype='text/csv')

@app.route(BASE_URL + "/download/all/<keyword>/<filename>", methods=['GET'])
def downloadall(keyword, filename):
  if not islogin(): return redirect(BASE_URL + '/login')
  return Response(download.download_all(keyword), mimetype='text/csv')

@app.route(BASE_URL + "/download/classified", methods=['GET'])
def downloadclassified():
  if not islogin(): return redirect(BASE_URL + '/login')
  tweets = dbr.get_search_instance(keyword = 'LEARN', enc = False).params(size = 1000111000).execute().hits
  return Response( json.dumps( [t.to_dict() for t in tweets] ) , mimetype='text/csv')



# DUMMY
@app.route(BASE_URL + "/reset")
def reset():
  if not islogin(): return redirect(BASE_URL + '/login')
  ret = dbk.db.update('keyword', {'processing': 0, 'since_id': 0, 'max_id': 0}, ('status = %s', ['active']) )
  dbk.db.commit()
  return json.dumps( ret )

from os import popen, system
@app.route(BASE_URL + "/add_streamer")
def add_streamer():
  if not islogin(): return redirect(BASE_URL + '/login')
  return json.dumps( system('python streamer/tweet_streamer.py &') )

@app.route(BASE_URL + "/streamer_status")
def streamer_status():
  if not islogin(): return redirect(BASE_URL + '/login')
  ret = ''
  for l in popen('ps aux | grep python').readlines(): ret += (l.strip() + '<br>')
  return ret

@app.route(BASE_URL + "/keep_streamer/<num>")
def keep_streamer(num):
  if not islogin(): return redirect(BASE_URL + '/login')
  active_count = len(popen('ps aux | grep "python streamer/tweet_streamer.py"').readlines())-1
  added = 0
  while active_count + added < int(num):
    add_streamer()
    added += 1
  return "%d streamer(s) added" % (added)


if len(sys.argv) > 1 and sys.argv[1] == "dev":
  if __name__ == "__main__":
    app.secret_key = 'hutlanggar17'
    app.run(host=HOST, port=PORT, debug=DEBUG)

from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop
from tornado import autoreload
from tornado.httpserver import HTTPServer

if __name__ == "__main__":
    app.secret_key = 'hutlanggar17'
    container = WSGIContainer(app)

    # app = Application([
    #     (r'.*', FallbackHandler, dict(fallback=container))
    # ])
    # server = HTTPServer(app)
    # server.bind(PORT)
    # server.start(0)
    # IOLoop.current().start()
    
    server = Application([
        (r'.*', FallbackHandler, dict(fallback=container))
    ])
    server.listen(PORT, address=HOST)
    ioloop = IOLoop.instance()
    autoreload.start(ioloop)
    ioloop.start()