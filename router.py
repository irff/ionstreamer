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

  # jangan diapa-apakan kalau di db lagi processing
  if sum([1 for x in dbk.get() if x.keyword == keyword and x.status != 'processing']):
    return "%s is processing" % keyword

  return json.dumps( dbk.set(request.json) )

@app.route("/api/summary", methods=['GET'])
def summary():
  keywords = [x for x in dbk.get() if x.status != 'removed']

  # sort row based on active/inactive
  def comp(x,y):
    xs = x.status
    ys = y.status
    if xs == 'processing': xs = 'active'
    if ys == 'processing': ys = 'active'
    return cmp((xs, x.keyword), (ys, y.keyword))
  keywords.sort(comp)

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


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
