from flask import Flask, render_template, redirect, request
app = Flask(__name__)


from config import *
from database.dbmysql import *

import json


@app.route("/")
def home():
    return render_template('streamings.html')

@app.route("/streamings")
def all_keyword():
  keywords = fetch(KEYWORD)

  # sort row based on active/inactive
  def comp(x,y):
    xs = x.status
    ys = y.status
    if xs == 'processing': xs = 'active'
    if ys == 'processing': ys = 'active'
    return cmp((xs, x.keyword), (ys, y.keyword))
  keywords.sort(comp)

  def getinfo(row):
    counts = count(RESULT, where = {'keyword': row.keyword})
    data = fetch(RESULT, where = {'keyword': row.keyword}, order = ['created_at', 'DESC'], limit = (0, 3))

    if len(data) < 3: return {'name': row.keyword, 'counts': 'no results yet', 'status': row.status, 'tw1': '', 'tw2': '', 'tw3': ''}
    return {'name': row.keyword, 'counts': '%d results'%counts, 'status': row.status, 'tw1': data[0].text, 'tw2': data[1].text, 'tw3': data[2].text}
  
  return json.dumps(map(getinfo, keywords))

# curl -XPOST localhost:7876/stream -d 'keyword=syawal&status=1'
@app.route("/stream", methods=['POST'])
def index_keyword():
  counts = count(KEYWORD, where = {'keyword': request.form['keyword'], 'status': 'processing'})
  
  if counts > 0:
    return request.form['keyword'] + "is processing!"

  return json.dumps(update(KEYWORD, request.form))

@app.route("/unstream", methods=['POST'])
def delete_keyword():
  return json.dumps(delete(KEYWORD, where = {'keyword': request.form['keyword']}))


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)