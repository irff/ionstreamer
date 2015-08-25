from config import DATABASE, USER, PASSWORD
from simplemysql import SimpleMysql
from time import time, sleep
from datetime import datetime, timedelta
from math import ceil
import sys

db = SimpleMysql(host="localhost", db=DATABASE, user=USER, passwd=PASSWORD, keep_alive=True)
TOKEN = "token"

def get():
  ret = db.getAll(table = TOKEN)
  db.commit()
  if ret == None: ret = []
  return ret

def setToken(data):
  ret = db.insertOrUpdate(table = TOKEN, data = data, keys = [])
  db.commit()
  return ret

def getOneToken():
  print "golek token.."
  try:
    while True:
      tokens = [x for x in get() if ( datetime.now() - x.last_used ) > timedelta(seconds = 6)]
      if len(tokens) > 0:
        setToken( {'CONSUMER_KEY': tokens[0].CONSUMER_KEY, 'last_used': datetime.fromtimestamp( ceil(time()) ).__str__()} )
        print "entuk token: %s" % (tokens[0].name)
        return tokens[0]
      sleep(1)
  except Exception as e:
    print >> sys.stderr, "token manager error: %s" % str(e)
    return None
