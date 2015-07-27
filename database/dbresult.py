from config import INDEX
from base64 import b64encode
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
es = Elasticsearch()

def set(keyword, data, enc = True):
  id = data['id_str']
  return es.index(index = INDEX, doc_type = b64encode(keyword) if enc else keyword, id = id, body=data)

def get(keyword, id, enc = True):
  return es.get(index = INDEX, doc_type = b64encode(keyword) if enc else keyword, id = id)

def delete(keyword, id, enc = True):
  return es.index(index = INDEX, doc_type = b64encode(keyword) if enc else keyword, id = id, ignore=404)

def get_search_instance(keyword = None, enc = True):
  if keyword == None:
    return Search(using = es, index = INDEX)
  else:
    return Search(using = es, index = INDEX, doc_type = b64encode(keyword) if enc else keyword)