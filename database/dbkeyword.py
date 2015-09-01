# from config import DATABASE, USER, PASSWORD
# from simplemysql import SimpleMysql
# from time import sleep
# import sys

# db = SimpleMysql(host="localhost", db=DATABASE, user=USER, passwd=PASSWORD, keep_alive=True)
# KEYWORD = "keyword"

# def get():
#   ret = db.getAll(table = KEYWORD)
#   db.commit()
#   if ret == None: ret = []
#   return ret

# def getOneKeyword():
#   print "golek keyword.."
#   try:
#     while True:
#       keywords = [x for x in get() if x.status == 'active' and not x.processing]
#       if len(keywords) > 0:
#         keywords.sort(key = lambda k: k.last_modified)
#         print "entuk keyword: %s" % (keywords[0].keyword)
#         return keywords[0]
#       sleep(1)
#   except Exception as e:
#     print >> sys.stderr, "keyword manager error: %s" % str(e)
#     return None

# def set(data):
#   ret = db.insertOrUpdate(table = KEYWORD, data = data, keys = [])
#   db.commit()
#   return ret

# def delete(keyword):
#   ret = db.delete(table = KEYWORD, where = ("keyword = %s", [keyword]))
#   db.commit()
#   return ret

from sys import stderr
from time import time, sleep
from config import INDEX, ESHOST
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
es = Elasticsearch(ESHOST, timeout = 60)
KEYWORD = "KEYWORD"

def getAll():
  try:
    return Search(using = es, index = INDEX, doc_type = KEYWORD).execute().hits
  except Exception as e:
    print "Exception: " + str(e)
    return []

def setData(data):
  old = {'status': 'inactive', 'processing': 0, 'since_id': 0, 'max_id': 0}
  try: old = es.get(index = INDEX, doc_type = KEYWORD, id = data['keyword'])['_source']
  except: pass
  for k in old:
    if k not in data:
      data[k] = old[k]
  if 'last_used' not in data: data['last_used'] = time()
  return es.index(index = INDEX, doc_type = KEYWORD, id = data['keyword'], body=data)

def getOne():
  try:
    while True:
      keywords = [x for x in getAll() if x.status == 'active' and not x.processing]
      if len(keywords) > 0:
        keyword = min(keywords, key = lambda k: k.last_used)
        keyword.last_used = time()
        setData( keyword.to_dict() )
        print "%s -" % (keyword.keyword),
        return keyword
      sleep(1)
  except Exception as e:
    print >> stderr, "keyword manager error: %s" % str(e)
    return None

def delete(keyword):
  try:
    return es.delete(index = INDEX, doc_type = KEYWORD, id = keyword)
  except Exception as e:
    print >> stderr, "delete keyword error: %s" % str(e)

def reset():
  for d in getAll():
    setData({'keyword': d.keyword, 'processing': 0, 'since_id': 0, 'max_id': 0})
  return 1
