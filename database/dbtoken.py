from simplemysql import SimpleMysql

db = SimpleMysql(host="localhost", db="ionstreamer", user="root", passwd="", keep_alive=True)

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