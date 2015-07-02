import database.dbtoken as dbt
from datetime import datetime, timedelta
from time import time, sleep

TOKEN = "token"

def gettoken(delta = 10):
  try:
    while True:
      tokens = [x for x in dbt.get() if x.usable and ( datetime.now() - x.last_used ) > timedelta(seconds = delta)]
      if len(tokens):
        dbt.set( {'CONSUMER_KEY': tokens[0].CONSUMER_KEY, 'last_used': datetime.fromtimestamp( round(time()) ).__str__()} )
        return tokens[0]
      sleep(.5)
  except Exception as e:
    print e
    return None
