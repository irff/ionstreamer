import database.dbtoken as dbt
from datetime import datetime, timedelta
from time import time, sleep
from math import ceil

TOKEN = "token"

def gettoken():
  print "golek token.."
  try:
    while True:
      tokens = [x for x in dbt.get() if ( datetime.now() - x.last_used ) > timedelta(seconds = 6)]
      if len(tokens) > 0:
        dbt.set( {'CONSUMER_KEY': tokens[0].CONSUMER_KEY, 'last_used': datetime.fromtimestamp( ceil(time()) ).__str__()} )
        print "entuk token: %s" % (tokens[0].name)
        return tokens[0]
      sleep(1)
  except Exception as e:
    print >> sys.stderr, "tokenmanager error: %s" % str(e)
    return None
