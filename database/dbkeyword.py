from config import DATABASE, USER, PASSWORD
from simplemysql import SimpleMysql
from time import sleep
import sys

db = SimpleMysql(host="localhost", db=DATABASE, user=USER, passwd=PASSWORD, keep_alive=True)
KEYWORD = "keyword"

def get():
  ret = db.getAll(table = KEYWORD)
  db.commit()
  if ret == None: ret = []
  return ret

def getOneKeyword():
  print "golek keyword.."
  try:
    while True:
      keywords = [x for x in get() if x.status == 'active' and not x.processing]
      if len(keywords) > 0:
        keywords.sort(key = lambda k: k.last_modified)
        print "entuk keyword: %s" % (keywords[0].keyword)
        return keywords[0]
      sleep(1)
  except Exception as e:
    print >> sys.stderr, "keyword manager error: %s" % str(e)
    return None

def set(data):
  ret = db.insertOrUpdate(table = KEYWORD, data = data, keys = [])
  db.commit()
  return ret

def delete(keyword):
  ret = db.delete(table = KEYWORD, where = ("keyword = %s", [keyword]))
  db.commit()
  return ret