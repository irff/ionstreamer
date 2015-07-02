from flask import Flask
import settings, os

if os.path.exists('dead'): os.remove('dead')




# initialize database
import sqlite3
db_session = sqlite3.connect('ionstreamer.db')
c = db_session.cursor()
q = "CREATE TABLE IF NOT EXISTS `streamings` (`keyword` varchar(64) NOT NULL, PRIMARY KEY (`keyword`) );"
# this line below will be remove if using elasticsearch
#q += "CREATE TABLE IF NOT EXISTS `results` ( `id` integer NOT NULL, `keyword` varchar(64) NOT NULL, `result` varchar(256), PRIMARY KEY (`id`) );"
for e in q.split(";"):
  c.execute(e)
db_session.commit()
db_session.close()





"""import all controller from application.controllers"""
from controllers.stream import stream
"""import more controller"""






app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

"""register each controller as blueprint"""
app.register_blueprint(stream)
"""register more controller"""

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     # open('dead', 'w').close()

if __name__ == '__main__':
  try:
    app.debug = True
    app.run(port=settings.PORT, host=settings.HOST)
  except Exception, e:
    pass
  finally:
    open('dead', 'w').close()