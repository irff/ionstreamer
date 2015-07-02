from flask import Flask, render_template, redirect, request
app = Flask(__name__)

# from elasticsearch import Elasticsearch
# es = Elasticsearch()

from simplemysql import SimpleMysql
db = SimpleMysql(host="localhost", db="ionstreamer", user="root", passwd="", keep_alive=True)


import config, json


@app.route("/")
def home():
    return render_template('streamings.html')

@app.route("/streamings")
def all_keyword():
  # try:
  #   keywords = es.search(index=config.INDEX, doc_type=config.KEYWORD)['hits']['hits']
  # except Exception, e:
  #   keywords = []
  # keywords = map(lambda x: (x['_id'], x['_source']['status']), keywords)
  keywords = db.getAll(config.KEYWORD)
  if keywords == None: keywords = []

  def getinfo(row):
    if row.status == 0: status = 'status: paused'
    if row.status == 1: status = 'status: active streaming'
    data = db.getAll(config.RESULT, ['text'], ("keyword = %s", [row.keyword]))
    if data == None: data = []
    if len(data) < 3: return {'name': row.keyword, 'counts': 'no results yet', 'status': status, 'tw1': '', 'tw2': '', 'tw3': ''}
    return {'name': row.keyword, 'counts': '%d results'%len(data), 'status': status, 'tw1': data[-3].text, 'tw2': data[-2].text, 'tw3': data[-1].text}
    # try:
    #   counts = es.count(index=config.INDEX, doc_type=config.RESULT, q='keyword:'+k)['count']
    #   top3 = es.search(index=config.INDEX, doc_type=config.RESULT, q='keyword:'+k, from_=counts-3)['hits']['hits']
    #   top3 = map(lambda x: x['_source']['text'], top3)
    #   return {'name': k, 'counts': '%d results'%counts, 'status': 'status: '+s, 'tw1': top3[0], 'tw2': top3[1], 'tw3': top3[2]}
    # except Exception, e:
    #   return {'name': k, 'counts': 'no results', 'status': 'status: '+s, 'tw1': '', 'tw2': '', 'tw3': ''}
  
  return json.dumps(map(getinfo, keywords))

@app.route("/stream", methods=['POST'])
def index_keyword():
  # return json.dumps(es.index(index=config.INDEX, doc_type=config.KEYWORD, id=request.form['keyword'].lower(), body={'status':request.form['status']}))
  ret = db.insertOrUpdate(config.KEYWORD, {"keyword": request.form['keyword'], "status": request.form['status']}, {})
  db.commit()
  return json.dumps(ret)

@app.route("/unstream", methods=['POST'])
def delete_keyword():
  # return json.dumps(es.delete(index=config.INDEX, doc_type=config.KEYWORD, id=request.form['keyword'].lower(), ignore=404))
  ret = db.delete(config.KEYWORD, ("keyword = %s", [request.form['keyword']]))
  db.commit()
  return json.dumps(ret)


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True)