import twitter

# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information 
# on Twitter's OAuth implementation.

CONSUMER_KEY = 'QggSVBP9t2RR4yzIvJpLHxHrL'
CONSUMER_SECRET ='ncRsiSeemxz02pEUMSRhVuEtKlWxFOyCPvCNwwWKL1cZQLY2TN'
OAUTH_TOKEN = '165650047-sNAi13v3VdDk8nhqMLmcdgTVzkR2Ton749BIntQ7'
OAUTH_TOKEN_SECRET = 'OM5JGhgswebcx8WYxn8yGrwPQdexb5VS00UIoguD117VU'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# Nothing to see by displaying twitter_api except that it's now a
# defined variable

r = twitter_api.search.tweets(q="jokowi")
for x in r['statuses']:
  print MySQLdb.escape_string(x['text'][:70])
