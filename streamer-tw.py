import twitter
CONSUMER_KEY = 'QggSVBP9t2RR4yzIvJpLHxHrL'
CONSUMER_SECRET ='ncRsiSeemxz02pEUMSRhVuEtKlWxFOyCPvCNwwWKL1cZQLY2TN'
OAUTH_TOKEN = '165650047-sNAi13v3VdDk8nhqMLmcdgTVzkR2Ton749BIntQ7'
OAUTH_TOKEN_SECRET = 'OM5JGhgswebcx8WYxn8yGrwPQdexb5VS00UIoguD117VU'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)
# res = twitter_api.search.tweets(q=keyword, count=5)['statuses']
# api call max 1 call / 5 seconds for safety


from simplemysql import SimpleMysql
db = SimpleMysql(host="localhost", db="ionstreamer", user="root", passwd="", keep_alive=True)


import config, time, datetime

data = {}

def gather(keyword):
  start = time.time()
  try: res = twitter_api.search.tweets(q=keyword, count=100)['statuses']
  except Exception, e: res = []

  res = map(lambda x:{
    'keyword': keyword,
    'text': x['text'],
    'created_at': x['created_at'],
    'username': x['user']['screen_name'],
    'name': x['user']['name'],
    'retweet_count': x['retweet_count']
    }, res)

  ret = 0
  for r in res:
    try:
      db.insert(config.RESULT, r)
      ret += 1
    except Exception, e:
      pass
  db.commit()


  print '+%d data about %s' % (ret, keyword)
  return time.time()-start



while True:
  keywords = db.getAll(config.KEYWORD)
  if keywords == None: keywords = []
  for k in keywords:
    if k.status == 1:
      time.sleep(7-gather(k.keyword))