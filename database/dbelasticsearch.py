from base64 import b64encode

from elasticsearch import Elasticsearch
es = Elasticsearch()

INDEX = "ionstreamer"

def dbget(table, limit = None, sort_by = "created_at:desc"):
  try:
    if limit >= 0:
      res = es.search(index=INDEX, doc_type=b64encode(table), sort=sort_by, size = limit)
    else:
      res = es.search(index=INDEX, doc_type=b64encode(table), sort=sort_by)
    return [x['_source'] for x in res['hits']['hits']]
  except Exception as e:
    print e
    return []

def dbcount(table):
  try:
    return es.search(index=INDEX, doc_type=b64encode(table))['hits']['total']
  except Exception as e:
    print e
    return 0

def dbset(table, data):
  id = data['id']
  return es.index(index = INDEX, doc_type = b64encode(table), id = id, body=data)

def dbdelete(table, id):
  return es.index(index = INDEX, doc_type = b64encode(table), id = id, ignore=404)