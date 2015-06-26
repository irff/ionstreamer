from base64 import b64encode, b64decode

from elasticsearch import Elasticsearch
es = Elasticsearch()

INDEX = "ionstreamer"

def _transform_where(where):
  if where == None: return None
  [k, v] = zip(*where.items())
  return (' and '.join([x+"=%s" for x in k]), v)


def fetch(table, where = None, order = None, limit = None):
  """ where berupa dict {attributes: values} """
  es.search(index = INDEX, doc_type = b64encode(table), )
  return ret

def update(table, data):
  es.index(index = INDEX, doc_type = b64encode(table), id = data['id'], body = data)

def delete(table, id):
  """ where berupa dict {attributes: values} """
  es.delete(index = INDEX, doc_type = b64encode(table), id = id)