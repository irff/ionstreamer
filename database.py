import sqlite3

db_session = sqlite3.connect('keywords.db')

c = db_session.cursor()

q = "CREATE TABLE IF NOT EXISTS `streamings` (`keyword` varchar(64) NOT NULL, PRIMARY KEY (`keyword`) );"
for e in q.split(";"):
  c.execute(e)

db_session.commit()

