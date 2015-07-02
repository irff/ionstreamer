from TwitterSearch import *
import time
try:
    tso = TwitterSearchOrder()
    tso.set_keywords(['to:jokowi', 'since:2015-6-23'])
    ts = TwitterSearch(
        consumer_key = 'QggSVBP9t2RR4yzIvJpLHxHrL',
        consumer_secret = 'ncRsiSeemxz02pEUMSRhVuEtKlWxFOyCPvCNwwWKL1cZQLY2TN',
        access_token = '165650047-sNAi13v3VdDk8nhqMLmcdgTVzkR2Ton749BIntQ7',
        access_token_secret = 'OM5JGhgswebcx8WYxn8yGrwPQdexb5VS00UIoguD117VU'
     )
    def my_callback_closure(current_ts_instance): # accepts ONE argument: an instance of TwitterSearch
        queries, tweets_seen = current_ts_instance.get_statistics()
        print queries
        if queries > 0 and (queries % 5) == 0: # trigger delay every 5th query
            time.sleep(1) # sleep for 60 seconds
    counter = 1
    for tweet in ts.search_tweets_iterable(tso, callback=my_callback_closure):
        print( '%d. [%s] @%s tweeted with id = %d' % ( counter, tweet['created_at'], tweet['user']['screen_name'], tweet['id'] ) )
        counter += 1
except TwitterSearchException as e:
    print(e)