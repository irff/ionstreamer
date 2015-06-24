from flask import Flask, render_template, redirect, request
app = Flask(__name__)


from simplemysql import SimpleMysql
db = SimpleMysql(host="localhost", db="ionstreamer", user="root", passwd="", keep_alive=True)


import config, json


@app.route("/")
def home():
    return render_template('streamings.html')

@app.route("/streamings")
def all_keyword():
  keywords = db.getAll(config.KEYWORD)
  db.commit()
  if keywords == None: keywords = []

  # sort row based on active/inactive
  def comp(x,y):
    xs = x.status
    ys = y.status
    if xs == 'processing': xs = 'active'
    if ys == 'processing': ys = 'active'
    return cmp((xs, x.keyword), (ys, y.keyword))
  keywords.sort(comp)

  def getinfo(row):
    data = db.getAll(config.RESULT, ['text'], ("keyword = %s", [row.keyword]), ['created_at', 'asc'])
    db.commit()
    if data == None: data = []
    if len(data) < 3: return {'name': row.keyword, 'counts': 'no results yet', 'status': row.status, 'tw1': '', 'tw2': '', 'tw3': ''}
    return {'name': row.keyword, 'counts': '%d results'%len(data), 'status': row.status, 'tw1': data[-1].text, 'tw2': data[-2].text, 'tw3': data[-3].text}
  
  return json.dumps(map(getinfo, keywords))

# curl -XPOST localhost:7876/stream -d 'keyword=syawal&status=1'
@app.route("/stream", methods=['POST'])
def index_keyword():
  # make sure it is now processing
  row = db.getOne(config.KEYWORD, ['status'], ("keyword = %s", [request.form['keyword']]))
  if row != None and row.status == 'processing': return request.form['keyword'] + 'is processing!'
  ret = db.insertOrUpdate(config.KEYWORD, request.form, {})
  db.commit()
  return json.dumps(ret)

@app.route("/unstream", methods=['POST'])
def delete_keyword():
  ret = db.delete(config.KEYWORD, ("keyword = %s", [request.form['keyword']]))
  db.commit()
  return json.dumps(ret)


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True)