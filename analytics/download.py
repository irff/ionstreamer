import sys, time, csv
import database.dbresult as dbr
import database.dbresultnews as dbrn

from os.path import abspath
from dateutil.parser import parse
from cStringIO import StringIO

sys.path.append(abspath(''))


def download_tweets_at(keyword, kelas, waktu1, waktu2):
  st = time.time()

  csvfile = StringIO()
  try:
    fieldnames = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
    w = csv.writer(csvfile)

    nomor = 0
    w.writerow(fieldnames)
    size = 10000
    while True:
      waktu1 = parse(waktu1)
      waktu2 = parse(waktu2)
      r = dbr.get_search_instance(keyword).params(size = size, from_ = nomor, fields='user.screen_name,user.name,text,created_at,retweet_count,favorite_count').filter('range', created_at = {'from': waktu1, 'to': waktu2}).execute()
      for t in r.hits:
        nomor += 1
        w.writerow([ str(nomor), '@' + t['user.screen_name'][0], t['user.name'][0].encode('utf-8'), t['text'][0].encode('utf-8'), t['created_at'][0][:10]+' '+t['created_at'][0][11:19], str(t['retweet_count'][0]), str(t['favorite_count'][0]) ])
      if len(r.hits) == 0: break
    
    print "%s %s %s %s - download tweets at: %lf" % (keyword, kelas, waktu1, waktu2, time.time() - st)
    return csvfile.getvalue()
  except Exception as e:
    return ''
  finally:
    csvfile.close()


def download_mention(keyword, username):
  st = time.time()

  csvfile = StringIO()
  try:
    fieldnames = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
    w = csv.writer(csvfile)

    nomor = 0
    w.writerow(fieldnames)
    size = 10000
    while True:
      r = dbr.get_search_instance(keyword).params(size = size, from_ = nomor, fields='user.screen_name,user.name,text,created_at,retweet_count,favorite_count').query('match', **{'entities.user_mentions.screen_name': username}).execute()
      for t in r.hits:
        nomor += 1
        w.writerow([ str(nomor), '@' + t['user.screen_name'][0], t['user.name'][0].encode('utf-8'), t['text'][0].encode('utf-8'), t['created_at'][0][:10]+' '+t['created_at'][0][11:19], str(t['retweet_count'][0]), str(t['favorite_count'][0]) ])
      if len(r.hits) == 0: break
    
    print "%s %s - download mention: %lf" % (keyword, username, time.time() - st)
    return csvfile.getvalue()
  except Exception as e:
    return ''
  finally:
    csvfile.close()


def download_posting(keyword, username):
  st = time.time()

  csvfile = StringIO()
  try:
    fieldnames = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
    w = csv.writer(csvfile)

    nomor = 0
    w.writerow(fieldnames)
    size = 10000
    while True:
      r = dbr.get_search_instance(keyword).params(size = size, from_ = nomor, fields='user.screen_name,user.name,text,created_at,retweet_count,favorite_count', sort='id_str:desc').query('match', **{'user.screen_name': username}).execute()
      for t in r.hits:
        nomor += 1
        w.writerow([ str(nomor), '@' + t['user.screen_name'][0], t['user.name'][0].encode('utf-8'), t['text'][0].encode('utf-8'), t['created_at'][0][:10]+' '+t['created_at'][0][11:19], str(t['retweet_count'][0]), str(t['favorite_count'][0]) ])
      if len(r.hits) == 0: break
    
    print "%s %s - download posting: %lf" % (keyword, username, time.time() - st)
    return csvfile.getvalue()
  except Exception as e:
    return ''
  finally:
    csvfile.close()


def download_hashtag(keyword, hashtag):
  st = time.time()

  csvfile = StringIO()
  try:
    fieldnames = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
    w = csv.writer(csvfile)

    nomor = 0
    w.writerow(fieldnames)
    size = 10000
    while True:
      r = dbr.get_search_instance(keyword).params(size = size, from_ = nomor, fields='user.screen_name,user.name,text,created_at,retweet_count,favorite_count').query('match', **{'entities.hashtags.text': hashtag}).execute()
      for t in r.hits:
        nomor += 1
        w.writerow([ str(nomor), '@' + t['user.screen_name'][0], t['user.name'][0].encode('utf-8'), t['text'][0].encode('utf-8'), t['created_at'][0][:10]+' '+t['created_at'][0][11:19], str(t['retweet_count'][0]), str(t['favorite_count'][0]) ])
      if len(r.hits) == 0: break
    
    print "%s %s - download hashtag: %lf" % (keyword, hashtag, time.time() - st)
    return csvfile.getvalue()
  except Exception as e:
    return ''
  finally:
    csvfile.close()


def download_all(keyword):
  st = time.time()

  csvfile = StringIO()
  try:
    fieldnames = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
    w = csv.writer(csvfile)

    nomor = 0
    w.writerow(fieldnames)
    size = 10000
    while True:
      r = dbr.get_search_instance(keyword).params(size = size, from_ = nomor, fields='user.screen_name,user.name,text,created_at,retweet_count,favorite_count').execute()
      for t in r.hits:
        nomor += 1
        w.writerow([ str(nomor), '@' + t['user.screen_name'][0], t['user.name'][0].encode('utf-8'), t['text'][0].encode('utf-8'), t['created_at'][0][:10]+' '+t['created_at'][0][11:19], str(t['retweet_count'][0]), str(t['favorite_count'][0]) ])
      if len(r.hits) == 0: break
    
    print "%s - download all: %lf" % (keyword, time.time() - st)
    return csvfile.getvalue()
  except Exception as e:
    return ''
  finally:
    csvfile.close()

def download_allnews(keyword):
  st = time.time()

  csvfile = StringIO()
  try:
    fieldnames = ['No.', 'Username', 'Name', 'Tweet', 'Created At', 'Retweet', 'Favorite']
    w = csv.writer(csvfile)

    nomor = 0
    w.writerow(fieldnames)
    size = 10000
    while True:
      r = dbrn.get_search_instance(keyword).params(size = size, from_ = nomor, fields='user.screen_name,user.name,text,created_at,retweet_count,favorite_count').execute()
      for t in r.hits:
        nomor += 1
        w.writerow([ str(nomor), '@' + t['user.screen_name'][0], t['user.name'][0].encode('utf-8'), t['text'][0].encode('utf-8'), t['created_at'][0][:10]+' '+t['created_at'][0][11:19], str(t['retweet_count'][0]), str(t['favorite_count'][0]) ])
      if len(r.hits) == 0: break
    
    print "%s - download all news: %lf" % (keyword, time.time() - st)
    return csvfile.getvalue()
  except Exception as e:
    return ''
  finally:
    csvfile.close()
