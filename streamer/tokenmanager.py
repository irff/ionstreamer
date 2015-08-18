import database.dbtoken as dbt
from datetime import datetime, timedelta
from time import time, sleep
from math import ceil

TOKEN = "token"

def gettoken(delta = 8): # 10 tokens, 5 streamers
  try:
    while True:
      tokens = [x for x in dbt.get() if ( datetime.now() - x.last_used ) > timedelta(seconds = delta)]
      if len(tokens):
        dbt.set( {'CONSUMER_KEY': tokens[0].CONSUMER_KEY, 'last_used': datetime.fromtimestamp( ceil(time()) ).__str__()} )
        return tokens[0]
      sleep(.5)
  except Exception as e:
    print >> sys.stderr, "tokenmanager error: %s" % str(e)
    return None