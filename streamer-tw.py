import twitter
CONSUMER_KEY = 'QggSVBP9t2RR4yzIvJpLHxHrL'
CONSUMER_SECRET ='ncRsiSeemxz02pEUMSRhVuEtKlWxFOyCPvCNwwWKL1cZQLY2TN'
OAUTH_TOKEN = '165650047-sNAi13v3VdDk8nhqMLmcdgTVzkR2Ton749BIntQ7'
OAUTH_TOKEN_SECRET = 'OM5JGhgswebcx8WYxn8yGrwPQdexb5VS00UIoguD117VU'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)
# res = twitter_api.search.tweets(q=keyword, count=100)['statuses']
# api call max 1 call / 5 seconds for safety

from elasticsearch import Elasticsearch
es = Elasticsearch()

import config, time, datetime


def gather(keyword):
  try:
    res = twitter_api.search.tweets(q=keyword, count=100)['statuses']
  except Exception, e:
    print e
    res = []

  res = map(lambda x:{
    'keyword': keyword,
    'text': x['text'],
    'created_at': x['created_at'],
    'username': x['user']['screen_name'],
    'name': x['user']['name'],
    'image': x['user']['profile_image_url'],
    }, res)

  try:
    prev_res = es.search(index=config.INDEX, doc_type=config.RESULT, sort='_id:desc', size=100, q=keyword)['hits']['hits']
  except Exception, e:
    prev_res = []
  prev_res = map(lambda x: (x['_source']['username'], x['_source']['text']), prev_res)

  res = filter(lambda x: (x['username'], x['text']) not in prev_res, res)

  ret = 0.
  for r in res:
    es.index(index=config.INDEX, doc_type=config.RESULT, id=datetime.datetime.now(), body=r)
    ret += .05
    time.sleep(.05)

  print '+%d data about %s' % (len(res), keyword)
  return ret



while True:
  try:
    keywords = es.search(index=config.INDEX, doc_type=config.KEYWORD)['hits']['hits']
  except Exception, e:
    keywords = []
  keywords = map(lambda x: x['_id'], keywords)
  for k in keywords:
    time.sleep(7-gather(k))