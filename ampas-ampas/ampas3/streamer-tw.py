import twitter
CONSUMER_KEY = 'QggSVBP9t2RR4yzIvJpLHxHrL'
CONSUMER_SECRET ='ncRsiSeemxz02pEUMSRhVuEtKlWxFOyCPvCNwwWKL1cZQLY2TN'
OAUTH_TOKEN = '165650047-sNAi13v3VdDk8nhqMLmcdgTVzkR2Ton749BIntQ7'
OAUTH_TOKEN_SECRET = 'OM5JGhgswebcx8WYxn8yGrwPQdexb5VS00UIoguD117VU'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)
# res = twitter_api.search.tweets(q=keyword, count=5)['statuses']
# api call max 1 call / 5 seconds for safety

# from elasticsearch import Elasticsearch
# es = Elasticsearch()
# NO MORE ELASTIC

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
    'image': x['user']['profile_image_url'],
    }, res)

  # if keyword not in data: data[keyword] = []
  # top100 = data[keyword]

  # for x in top100: print str(x)[:70]+str(x)[-70:]
  # print ""
  # for x in [(y['username'], y['text']) for y in res]: print str(x)[:70]+str(x)[-70:]
  # print "--"*70

  # res = filter(lambda x: (x['username'], x['text']) not in top100, res)

  ret = 0
  for r in res:
    # es.index(index=config.INDEX, doc_type=config.RESULT, id=str(datetime.datetime.now()), body=r)
    try:
      db.insert(config.RESULT, r)
      ret += 1
    except Exception, e:
      # print e
      pass
  db.commit()

  # top100.extend(res)
  # del top100[:-100]

  print '+%d data about %s' % (ret, keyword)
  # return time.time()-start
  return 1


#ambil semua result dari masing-masing keyword
#sisakan 100 data terakhir saja
# try: keywords = es.search(index=config.INDEX, doc_type=config.KEYWORD, q='status:1')['hits']['hits']
# except Exception, e: keywords = []
# keywords = map(lambda x: x['_id'], keywords)
# keywords = db.getAll(config.KEYWORD)
# if keywords == None: keywords = []

# for k in keywords:
#   try:
#     res = es.search(index=config.INDEX, doc_type=config.RESULT, q='keyword:'+k)['hits']['hits']
#     data[k] = map(lambda x: (x['_source']['username'], x['_source']['text']), res)
#   except Exception, e:
#     data[k] = []
#     time.sleep(.1)
#   del data[k][:-100]


while True:
  # try: keywords = es.search(index=config.INDEX, doc_type=config.KEYWORD, q='status:1')['hits']['hits']
  # except Exception, e: keywords = []
  # keywords = map(lambda x: x['_id'], keywords)
  keywords = db.getAll(config.KEYWORD)
  if keywords == None: keywords = []
  for k in keywords:
    if k.status == 1:
      time.sleep(7-gather(k.keyword))