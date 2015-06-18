from flask import Flask
app = Flask(__name__)

from elasticsearch import Elasticsearch
es = Elasticsearch()

import config


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/stream")
def all_keyword():
  return map(lambda x: x['_id'], es.search(index=config.INDEX, doc_type='keyword')['hits']['hits']).__str__()

@app.route("/stream/<keyword>")
def index_keyword(keyword):
  return es.index(index=config.INDEX, doc_type='keyword', id=keyword, body={}).__str__()

@app.route("/unstream/<keyword>")
def delete_keyword(keyword):
  return es.delete(index=config.INDEX, doc_type='keyword', id=keyword).__str__()

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True)