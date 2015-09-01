# from config import DATABASE, USER, PASSWORD
# from simplemysql import SimpleMysql
# from time import time, sleep
# from datetime import datetime, timedelta
# from math import ceil
# import sys

# db = SimpleMysql(host="localhost", db=DATABASE, user=USER, passwd=PASSWORD, keep_alive=True)
# TOKEN = "token"

# def get():
#   ret = db.getAll(table = TOKEN)
#   db.commit()
#   if ret == None: ret = []
#   return ret

# def setToken(data):
#   ret = db.insertOrUpdate(table = TOKEN, data = data, keys = [])
#   db.commit()
#   return ret

# def getOneToken():
#   print "golek token.."
#   try:
#     while True:
#       tokens = [x for x in get() if ( datetime.now() - x.last_used ) > timedelta(seconds = 6)]
#       if len(tokens) > 0:
#         setToken( {'CONSUMER_KEY': tokens[0].CONSUMER_KEY, 'last_used': datetime.fromtimestamp( ceil(time()) ).__str__()} )
#         print "entuk token: %s" % (tokens[0].name)
#         return tokens[0]
#       sleep(1)
#   except Exception as e:
#     print >> sys.stderr, "token manager error: %s" % str(e)
#     return None


from sys import stderr
from time import time, sleep
from config import INDEX, ESHOST
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
es = Elasticsearch(ESHOST, timeout = 60)
TOKEN = "TOKEN"

def getAll():
  try:
    return Search(using = es, index = INDEX, doc_type = TOKEN).execute().hits
  except Exception as e:
    print "Exception: " + str(e)
    return []

def setData(data):
  old = {'name': 'ionstreamer-n'}
  try: old = es.get(index = INDEX, doc_type = TOKEN, id = data['CONSUMER_KEY'])['_source']
  except: pass
  for k in old:
    if k not in data:
      data[k] = old[k]
  if 'last_used' not in data: data['last_used'] = time()
  return es.index(index = INDEX, doc_type = TOKEN, id = data['CONSUMER_KEY'], body=data)

def getOne():
  try:
    while True:
      tokens = [x for x in getAll() if time() - x.last_used > 6.]
      if len(tokens) > 0:
        token = min(tokens, key = lambda k: k.last_used)
        token.last_used = time()
        setData( token.to_dict() )
        print "token: %s" % (token.name)
        return token
      sleep(1)
  except Exception as e:
    print >> stderr, "token manager error: %s" % str(e)
    return None

def delete(keyword):
  try:
    return es.delete(index = INDEX, doc_type = TOKEN, id = keyword)
  except Exception as e:
    print >> stderr, "delete keyword error: %s" % str(e)
