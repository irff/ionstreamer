from base64 import b64encode

from elasticsearch import Elasticsearch
es = Elasticsearch()

INDEX = "ionstreamer"

def get(keyword, size, timeout = 60):
  try:
    res = es.search(index=INDEX, doc_type=b64encode(keyword), size = size, timeout = timeout)
    return [x['_source'] for x in res['hits']['hits']]
  except Exception as e:
    print e
    return []

def get_fields(keyword, size, fields, timeout = 60):
  try:
    res = es.search(index=INDEX, doc_type=b64encode(keyword), size = size, fields = fields, timeout = timeout)
    return [x['fields'] for x in res['hits']['hits'] if 'fields' in x]
  except Exception as e:
    print e
    return []

def count(keyword):
  try:
    return es.count(index=INDEX, doc_type=b64encode(keyword))['count']
  except Exception as e:
    print e
    return 0

def set(keyword, data):
  id = data['id']
  return es.index(index = INDEX, doc_type = b64encode(keyword), id = id, body=data)

def delete(keyword, id):
  return es.index(index = INDEX, doc_type = b64encode(keyword), id = id, ignore=404)