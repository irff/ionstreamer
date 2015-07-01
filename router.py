from flask import Flask, render_template, redirect, request
app = Flask(__name__)


from config import *
from database.dbmysql import *
import database.dbelasticsearch as dbes

import json


@app.route("/")
def home():
    return render_template('streamings.html')

# API
@app.route("/api/stream", methods=['POST'])
def apistream():
  keyword = request.json['keyword']
  status = request.json['status']

  # jangan diapa-apakan kalau di db lagi processing
  if dbcount(KEYWORD, {'keyword': keyword, 'status': 'processing'}):
    return "%s is processing" % keyword

  return json.dumps( dbset(KEYWORD, request.json) )

@app.route("/api/summary", methods=['GET'])
def summary():
  keywords = [x for x in dbget(KEYWORD) if x.status != 'removed']

  # sort row based on active/inactive
  def comp(x,y):
    xs = x.status
    ys = y.status
    if xs == 'processing': xs = 'active'
    if ys == 'processing': ys = 'active'
    return cmp((xs, x.keyword), (ys, y.keyword))
  keywords.sort(comp)

  def getinfo(row):
    count = dbes.dbcount(row.keyword)
    data = dbes.dbget(row.keyword)
    data.sort(lambda x,y: cmp(y['created_at'],x['created_at']))

    if len(data) == 0: return {'keyword': row.keyword, 'count': 'no results yet', 'status': row.status, 'tweets': []}
    return {'keyword': row.keyword, 'count': '%d results'%count, 'status': row.status, 'tweets': ["@%s: %s"%(d['user']['screen_name'],d['text']) for d in data[:3]]}

  return json.dumps( map(getinfo, keywords) )


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
