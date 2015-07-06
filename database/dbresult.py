INDEX = "ionstreamer2.1"

from base64 import b64encode

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
es = Elasticsearch()

def set(keyword, data):
  id = data['id_str']
  return es.index(index = INDEX, doc_type = b64encode(keyword), id = id, body=data)

def delete(keyword, id):
  return es.index(index = INDEX, doc_type = b64encode(keyword), id = id, ignore=404)

def get_search_instance(keyword):
  return Search(using = es, index = INDEX, doc_type = b64encode(keyword))