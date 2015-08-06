from flask import Flask, render_template, request, Response, session, abort, redirect
app = Flask(__name__)

from config import DEBUG, HOST, PORT, BASE_URL
import database.dbkeyword as dbk
import database.dbresult as dbr
import analytics.tweet as tweeta

import json, sys

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
    if username == 'langgar' and password == 'hutlanggar17':
      session['username'] = request.form['username']
      return redirect(BASE_URL + '/')
    else:
      return showlogin(username = request.form.get('username'))
  except Exception as e:
    return abort(404)

@app.route(BASE_URL + "/logout", methods = ['GET'])
def logout():
  session.pop('username', None)
  return redirect(BASE_URL + '/login')


@app.route(BASE_URL + "/analyze/<keyword>")
def showanalyze(keyword):
  if not islogin(): return redirect(BASE_URL + '/login')
  return render_template('analyze.html', keyword = keyword, nav = 'analyze')

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
  size = dbr.get_search_instance('LEARN', enc = False).params(search_type = 'count', size = 0).execute().hits.total
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
  if not islogin(): return redirect(BASE_URL + '/login')
  keyword = request.json['keyword']
  status = request.json['status']
  if any([x.keyword == keyword and x.processing for x in dbk.get()]):
    return "%s is processing" % keyword
  return json.dumps( dbk.set(request.json) )

@app.route(BASE_URL + "/api/summary", methods=['GET'])
def summary():
  if not islogin(): return redirect(BASE_URL + '/login')
  keywords = [x for x in dbk.get() if x.status != 'removed']
  keywords.sort(lambda x, y: cmp(x.status, y.status))
  return json.dumps( map(tweeta.getinfo, keywords) )

@app.route(BASE_URL + "/api/analyze/freq/<keyword>", methods=['GET'])
def apianalyze(keyword):
  if not islogin(): return redirect(BASE_URL + '/login')
  return json.dumps( tweeta.get_tweet_freq(keyword) )

@app.route(BASE_URL + "/api/analyze/topmentions/<keyword>", methods=['GET'])
def topmentions(keyword):
  if not islogin(): return redirect(BASE_URL + '/login')
  return json.dumps( tweeta.get_top_mentions(keyword) )

@app.route(BASE_URL + "/api/analyze/toppostings/<keyword>", methods=['GET'])
def toppostings(keyword):
  if not islogin(): return redirect(BASE_URL + '/login')
  return json.dumps( tweeta.get_top_postings(keyword) )

@app.route(BASE_URL + "/api/analyze/topretweets/<keyword>", methods=['GET'])
def topretweets(keyword):
  if not islogin(): return redirect(BASE_URL + '/login')
  return json.dumps( tweeta.get_top_retweets(keyword) )

@app.route(BASE_URL + "/api/analyze/randomtweets/<keyword>", methods=['GET'])
def randomtweets(keyword):
  if not islogin(): return redirect(BASE_URL + '/login')
  return json.dumps( tweeta.get_random_tweets(keyword) )

@app.route(BASE_URL + "/api/analyze/gettweetsat/<keyword>/<kelas>/<waktu1>/<waktu2>", methods=['GET'])
def gettweetsat(keyword, kelas, waktu1, waktu2):
  if not islogin(): return redirect(BASE_URL + '/login')
  return json.dumps( tweeta.get_tweets_at(keyword, kelas, waktu1, waktu2) )

@app.route(BASE_URL + "/api/analyze/getmentions/<keyword>/<username>", methods=['GET'])
def getmentions(keyword, username):
  if not islogin(): return redirect(BASE_URL + '/login')
  return json.dumps( tweeta.get_mentions(keyword, username) )

@app.route(BASE_URL + "/api/analyze/getpostings/<keyword>/<username>", methods=['GET'])
def getpostings(keyword, username):
  if not islogin(): return redirect(BASE_URL + '/login')
  return json.dumps( tweeta.get_postings(keyword, username) )


# DOWNLOAD
@app.route(BASE_URL + "/download/tweetsat/<keyword>/<kelas>/<waktu1>/<waktu2>/<filename>", methods=['GET'])
def downloadtweetsat(keyword, kelas, waktu1, waktu2, filename):
  if not islogin(): return redirect(BASE_URL + '/login')
  return Response(tweeta.download_tweets_at(keyword, kelas, waktu1, waktu2), mimetype='text/csv')

@app.route(BASE_URL + "/download/mentions/<keyword>/<username>/<filename>", methods=['GET'])
def downloadmentions(keyword, username, filename):
  if not islogin(): return redirect(BASE_URL + '/login')
  return Response(tweeta.download_mentions(keyword, username), mimetype='text/csv')

@app.route(BASE_URL + "/download/postings/<keyword>/<username>/<filename>", methods=['GET'])
def downloadpostings(keyword, username, filename):
  if not islogin(): return redirect(BASE_URL + '/login')
  return Response(tweeta.download_postings(keyword, username), mimetype='text/csv')

@app.route(BASE_URL + "/download/all/<keyword>/<filename>", methods=['GET'])
def downloadall(keyword, filename):
  if not islogin(): return redirect(BASE_URL + '/login')
  return Response(tweeta.download_all(keyword), mimetype='text/csv')



# DUMMY
@app.route(BASE_URL + "/reset")
def reset():
  if not islogin(): return redirect(BASE_URL + '/login')
  ret = dbk.db.update('keyword', {'processing': 0, 'since_id': 0, 'max_id': 0}, ('status = %s', ['active']) )
  dbk.db.commit()
  return json.dumps( ret )


if __name__ == "__main__":
  app.secret_key = 'hutlanggar17'
  app.run(host=HOST, port=PORT, debug=DEBUG)

# from tornado.wsgi import WSGIContainer
# from tornado.web import Application, FallbackHandler
# from tornado.ioloop import IOLoop
# from tornado import autoreload
# from tornado.httpserver import HTTPServer

# if __name__ == "__main__":
#     container = WSGIContainer(app)
#     app = Application([
#         (r'.*', FallbackHandler, dict(fallback=container))
#     ])
#     server = HTTPServer(app)
#     server.bind(PORT)
#     server.start(0)
#     IOLoop.current().start()
    
    # server = Application([
    #     (r'.*', FallbackHandler, dict(fallback=container))
    # ])
    # server.listen(PORT, address=HOST)
    # ioloop = IOLoop.instance()
    # autoreload.start(ioloop)
    # ioloop.start()