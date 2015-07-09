from config import DATABASE, USER, PASSWORD
from simplemysql import SimpleMysql

db = SimpleMysql(host="localhost", db=DATABASE, user=USER, passwd=PASSWORD, keep_alive=True)

TOKEN = "token"

def get():
  ret = db.getAll(table = TOKEN)
  db.commit()
  if ret == None: ret = []
  return ret

def set(data):
  ret = db.insertOrUpdate(table = TOKEN, data = data, keys = [])
  db.commit()
  return ret