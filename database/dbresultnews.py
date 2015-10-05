from config import INDEX_NEWS, ESHOST
from base64 import b64encode
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
es = Elasticsearch(ESHOST, timeout = 60)

s = Search(using = es, index = INDEX_NEWS)

def setData(keyword, data, enc = True):
  id = data['url']
  return es.index(index = INDEX_NEWS, doc_type = b64encode(keyword) if enc else keyword, id = id, body=data)

def get(keyword, id, enc = True):
  return es.get(index = INDEX_NEWS, doc_type = b64encode(keyword) if enc else keyword, id = id)

def delete(keyword, id, enc = True):
  return es.delete(index = INDEX_NEWS, doc_type = b64encode(keyword) if enc else keyword, id = id, ignore=404)

def get_search_instance(keyword = None, enc = True):
  if keyword == None:
    return Search(using = es, index = INDEX_NEWS)
  else:
    return Search(using = es, index = INDEX_NEWS, doc_type = b64encode(keyword) if enc else keyword)