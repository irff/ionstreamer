from simplemysql import SimpleMysql
db = SimpleMysql(host="localhost", db="ionstreamer", user="root", passwd="", keep_alive=True)

def _transform_where(where):
  if where == None: return None
  [k, v] = zip(*where.items())
  return (' and '.join([x+"=%s" for x in k]), v)


def fetch(table, where = None, order = None, limit = None):
  """ where berupa dict {attributes: values} """
  ret = db.getAll(table = table, where = _transform_where(where), order = order, limit = limit)

  db.commit()

  if ret == None: ret = []

  return ret

def count(table, where):
  """ where berupa dict {attributes: values} """
  (where_str, values) = _transform_where(where)

  ret = db.query("SELECT COUNT(*) FROM %s WHERE %s" % (table, where_str), values).fetchone()[0]

  db.commit()

  return ret

def update(table, data):
  ret = db.insertOrUpdate(table = table, data = data, keys = [])

  db.commit()

  return ret

def delete(table, where = None):
  """ where berupa dict {attributes: values} """
  ret = db.delete(table = table, where = _transform_where(where))

  db.commit()

  return ret