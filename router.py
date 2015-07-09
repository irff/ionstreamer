from flask import Flask, render_template, request
app = Flask(__name__)

from config import HOST, PORT
import database.dbkeyword as dbk
import database.dbresult as dbr
import analytics.tweet as tweeta

import json, urllib

@app.route("/")
def home():
    return render_template('streamings.html')

@app.route("/analyze/<keyword>")
def analyze(keyword):
  return render_template('analyze.html', keyword = keyword, encoded_keyword = urllib.quote(keyword, safe='~()*!.\''))


# API
@app.route("/api/stream", methods=['POST'])
def apistream():
  keyword = request.json['keyword']
  status = request.json['status']
  if any([x.keyword == keyword and x.processing for x in dbk.get()]):
    return "%s is processing" % keyword
  return json.dumps( dbk.set(request.json) )

@app.route("/api/summary", methods=['GET'])
def summary():
  keywords = [x for x in dbk.get() if x.status != 'removed']
  keywords.sort(lambda x, y: cmp(x.status, y.status))
  return json.dumps( map(tweeta.getinfo, keywords) )

@app.route("/api/analyze/freq/<keyword>", methods=['GET'])
def apianalyze(keyword):
  return json.dumps( tweeta.get_tweet_freq(keyword) )

@app.route("/api/analyze/topmentions/<keyword>", methods=['GET'])
def topmentions(keyword):
  return json.dumps( tweeta.get_top_mentions(keyword) )

@app.route("/api/analyze/toppostings/<keyword>", methods=['GET'])
def toppostings(keyword):
  return json.dumps( tweeta.get_top_postings(keyword) )

@app.route("/api/analyze/topretweets/<keyword>", methods=['GET'])
def topretweets(keyword):
  return json.dumps( tweeta.get_top_retweets(keyword) )

@app.route("/api/analyze/randomtweets/<keyword>", methods=['GET'])
def randomtweets(keyword):
  return json.dumps( tweeta.get_random_tweets(keyword) )

@app.route("/api/analyze/gettweetsat/<keyword>/<waktu>", methods=['GET'])
def gettweetsat(keyword, waktu):
  return json.dumps( tweeta.get_tweets_at(keyword, waktu) )

@app.route("/api/analyze/getmentions/<keyword>/<username>", methods=['GET'])
def getmentions(keyword, username):
  return json.dumps( tweeta.get_mentions(keyword, username) )

@app.route("/api/analyze/getpostings/<keyword>/<username>", methods=['GET'])
def getpostings(keyword, username):
  return json.dumps( tweeta.get_postings(keyword, username) )


# DUMMY
@app.route("/reset")
def reset():
  ret = dbk.db.update('keyword', {'processing': 0, 'since_id': 0, 'max_id': 0}, ('status = %s', ['active']) )
  dbk.db.commit()
  return json.dumps( ret )

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)