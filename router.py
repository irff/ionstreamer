from flask import Flask, render_template
app = Flask(__name__)

from elasticsearch import Elasticsearch
es = Elasticsearch()

import config


@app.route("/")
def hello():
    return render_template('streamings.html')

@app.route("/streamings")
def all_keyword():
  try:
    ret = es.search(index=config.INDEX, doc_type=config.KEYWORD)['hits']['hits']
  except Exception, e:
    ret = []
  return map(lambda x: x['_id'], ret).__str__()

@app.route("/stream/<keyword>")
def index_keyword(keyword):
  return es.index(index=config.INDEX, doc_type=config.KEYWORD, id=keyword, body={}).__str__()

@app.route("/unstream/<keyword>")
def delete_keyword(keyword):
  return es.delete(index=config.INDEX, doc_type=config.KEYWORD, id=keyword, ignore=404).__str__()

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True)