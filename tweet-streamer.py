import config, time, datetime

from TwitterSearch import TwitterSearchOrder, TwitterSearch
ts = TwitterSearch(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET)

from simplemysql import SimpleMysql
db = SimpleMysql(host="localhost", db="ionstreamer", user="root", passwd="", keep_alive=True, charset='utf8', use_unicode=True)



attributes = ['keyword', 'text', 'created_at', 'username', 'name', 'retweet_count']
# tmp = {}
before_days = datetime.timedelta(30) # 30 days

def gather(row):
  print "gathering " + str(row) + "..."
  tso = TwitterSearchOrder()
  tso.set_keywords(['from:'+row.keyword, 'to:'+row.keyword], or_operator = True)
  if row.max_id > 0: tso.set_since_id(row.max_id)

  success = 0
  try:
    result = ts.search_tweets(tso)
    tweets = map(lambda x: {'keyword': row.keyword, 'text': x['text'], 'created_at': x['created_at'], 'username': x['user']['screen_name'],
      'name': x['user']['name'], 'retweet_count': x['retweet_count']}, result['content']['statuses'])
  except Exception as e: tweets = []

  if len(tweets) > 0:
    # since_id = result['content']['statuses'][0]['id']
    max_id = result['content']['statuses'][0]['id']
    db.update(config.KEYWORD, {'max_id': max_id}, ("keyword = %s", [row.keyword]))
  # for t in tweets: db.insert(config.RESULT, t)
  for t in tweets: db.insertOrUpdate(config.RESULT, t, {})
  db.commit()
  print "%s: +%d" % (row.keyword, len(tweets))


  ##################################################################################################################################
  # this is for past streaming
  ##################################################################################################################################
  # tso.add_keyword(['since:'+(row.datestamp-before_days).__str__()])
  # success = 0
  
  # def my_callback_closure(current_ts_instance): # accepts ONE argument: an instance of TwitterSearch
  #   db.commit()
  #   print '+%d data about %s' % (success, row.keyword)
  #   success = 0

  #   queries, tweets_seen = current_ts_instance.get_statistics()
  #   if queries > 0 and (queries % 5) == 0: # trigger delay every 5th query
  #     time.sleep(60) # sleep for 60 seconds
  
  # for tweet in ts.search_tweets_iterable(tso, callback=my_callback_closure):
  #   # print( '[%s] @%s tweeted: %s' % ( tweet['created_at'], tweet['user']['screen_name'], tweet['text'][:80] ) )
  #   for atr in attributes: tmp[atr] = tweet[atr]
  #   try:
  #     db.insert(config.RESULT, tmp)
  #     success += 1
  #   except Exception as e: pass
  # db.commit()
  # print '+%d data about %s' % (success, row.keyword)
  ##################################################################################################################################
  



while True:
  keywords = db.getAll(config.KEYWORD)
  db.commit()
  if keywords == None: keywords = []
  for k in keywords:
    if k.status == 1:
      gather(k)
      time.sleep(5.9)