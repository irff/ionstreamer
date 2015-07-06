from flask import Flask, render_template, request
app = Flask(__name__)


from config import *
import database.dbkeyword as dbk
import database.dbresult as dbr

import json, urllib
import analytics.tweet as tweeta


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

@app.route("/api/analyze/topmention/<keyword>", methods=['GET'])
def topmention(keyword):
  return json.dumps( tweeta.get_top_mention(keyword) )

@app.route("/api/analyze/topposting/<keyword>", methods=['GET'])
def topposting(keyword):
  return json.dumps( tweeta.get_top_posting(keyword) )

@app.route("/api/analyze/topretweet/<keyword>", methods=['GET'])
def topretweet(keyword):
  return json.dumps( tweeta.get_top_retweet(keyword) )


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
