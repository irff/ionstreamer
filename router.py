from flask import Flask, render_template, request, Response
app = Flask(__name__)

from config import DEBUG, HOST, PORT, BASE_URL
import database.dbkeyword as dbk
import database.dbresult as dbr
import analytics.tweet as tweeta

import json, sys

@app.route(BASE_URL + "/")
def showhome():
    return render_template('streamings.html', nav = 'home')

@app.route(BASE_URL + "/analyze/<keyword>")
def showanalyze(keyword):
  return render_template('analyze.html', keyword = keyword, nav = 'analyze')

@app.route(BASE_URL + "/learn", methods=['GET'])
def showlearn():
  return render_template('learn.html', nav = 'learn')

@app.route(BASE_URL + "/learn/<keyword>", methods=['GET'])
def showlearn_keyword(keyword):
  return render_template('learn.html', nav = 'learn', keyword = keyword)

@app.route(BASE_URL + "/learn/classified", methods=['GET'])
def showlearned():
  size = dbr.get_search_instance('LEARN', enc = False).params(search_type = 'count', size = 0).execute().hits.total
  return render_template('classified.html', nav = 'learn', size = size)


# LEARN
@app.route(BASE_URL + "/learn", methods=['POST'])
def learn():
  try:
    dbr.set('LEARN', request.json, enc = False)
    return "%s classified to %s" % (request.json['id_str'], request.json['class'])
  except Exception as e:
    print >> sys.stderr, "error: " + str(e)

@app.route(BASE_URL + "/learn/randomtweets", methods=['GET'])
@app.route(BASE_URL + "/learn/randomtweets/<keyword>", methods=['GET'])
def getrandomtweets(keyword = None, count = 10):
  print "KEYWORD %s" % keyword
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
  s = dbr.get_search_instance('LEARN', enc = False).params(size = size, from_ = offset)
  r = s.execute()
  return json.dumps(map(lambda x: x.to_dict(), r.hits))




# API
@app.route(BASE_URL + "/api/stream", methods=['POST'])
def apistream():
  keyword = request.json['keyword']
  status = request.json['status']
  if any([x.keyword == keyword and x.processing for x in dbk.get()]):
    return "%s is processing" % keyword
  return json.dumps( dbk.set(request.json) )

@app.route(BASE_URL + "/api/summary", methods=['GET'])
def summary():
  keywords = [x for x in dbk.get() if x.status != 'removed']
  keywords.sort(lambda x, y: cmp(x.status, y.status))
  return json.dumps( map(tweeta.getinfo, keywords) )

@app.route(BASE_URL + "/api/analyze/freq/<keyword>", methods=['GET'])
def apianalyze(keyword):
  return json.dumps( tweeta.get_tweet_freq(keyword) )

@app.route(BASE_URL + "/api/analyze/topmentions/<keyword>", methods=['GET'])
def topmentions(keyword):
  return json.dumps( tweeta.get_top_mentions(keyword) )

@app.route(BASE_URL + "/api/analyze/toppostings/<keyword>", methods=['GET'])
def toppostings(keyword):
  return json.dumps( tweeta.get_top_postings(keyword) )

@app.route(BASE_URL + "/api/analyze/topretweets/<keyword>", methods=['GET'])
def topretweets(keyword):
  return json.dumps( tweeta.get_top_retweets(keyword) )

@app.route(BASE_URL + "/api/analyze/randomtweets/<keyword>", methods=['GET'])
def randomtweets(keyword):
  return json.dumps( tweeta.get_random_tweets(keyword) )

@app.route(BASE_URL + "/api/analyze/gettweetsat/<keyword>/<kelas>/<waktu1>/<waktu2>", methods=['GET'])
def gettweetsat(keyword, kelas, waktu1, waktu2):
  return json.dumps( tweeta.get_tweets_at(keyword, kelas, waktu1, waktu2) )

@app.route(BASE_URL + "/api/analyze/getmentions/<keyword>/<username>", methods=['GET'])
def getmentions(keyword, username):
  return json.dumps( tweeta.get_mentions(keyword, username) )

@app.route(BASE_URL + "/api/analyze/getpostings/<keyword>/<username>", methods=['GET'])
def getpostings(keyword, username):
  return json.dumps( tweeta.get_postings(keyword, username) )


# DOWNLOAD
@app.route(BASE_URL + "/download/tweetsat/<keyword>/<kelas>/<waktu1>/<waktu2>/<filename>", methods=['GET'])
def downloadtweetsat(keyword, kelas, waktu1, waktu2, filename):
  return Response(tweeta.download_tweets_at(keyword, kelas, waktu1, waktu2), mimetype='text/csv')

@app.route(BASE_URL + "/download/mentions/<keyword>/<username>/<filename>", methods=['GET'])
def downloadmentions(keyword, username, filename):
  return Response(tweeta.download_mentions(keyword, username), mimetype='text/csv')

@app.route(BASE_URL + "/download/postings/<keyword>/<username>/<filename>", methods=['GET'])
def downloadpostings(keyword, username, filename):
  return Response(tweeta.download_postings(keyword, username), mimetype='text/csv')

@app.route(BASE_URL + "/download/all/<keyword>/<filename>", methods=['GET'])
def downloadall(keyword, filename):
  return Response(tweeta.download_all(keyword), mimetype='text/csv')



# DUMMY
@app.route(BASE_URL + "/reset")
def reset():
  ret = dbk.db.update('keyword', {'processing': 0, 'since_id': 0, 'max_id': 0}, ('status = %s', ['active']) )
  dbk.db.commit()
  return json.dumps( ret )



if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)