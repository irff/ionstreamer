from config import *
from database.dbmysql import *
from datetime import datetime, timedelta
from time import time, sleep

def gettoken():
  try:
    while True:
      # print dbget(TOKEN)
      tokens = [x for x in dbget(TOKEN) if x.usable and ( datetime.now() - x.last_used ) > timedelta(seconds = 5)]
      if len(tokens):
        dbset(TOKEN, {'CONSUMER_KEY': tokens[0].CONSUMER_KEY, 'last_used': datetime.fromtimestamp( round(time()) ).__str__()})
        return tokens[0]
      sleep(.5)
  except Exception as e:
    print e
    return None