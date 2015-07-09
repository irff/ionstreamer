from config import DATABASE, USER, PASSWORD
from simplemysql import SimpleMysql

db = SimpleMysql(host="localhost", db=DATABASE, user=USER, passwd=PASSWORD, keep_alive=True)

KEYWORD = "keyword"

def get():
  ret = db.getAll(table = KEYWORD)
  db.commit()
  if ret == None: ret = []
  return ret

def set(data):
  ret = db.insertOrUpdate(table = KEYWORD, data = data, keys = [])
  db.commit()
  return ret

def delete(keyword):
  ret = db.delete(table = KEYWORD, where = ("keyword = %s", [keyword]))
  db.commit()
  return ret