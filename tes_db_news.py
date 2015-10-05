# from config import ESHOST_NEWS
# from base64 import b64encode
# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search
# es = Elasticsearch(ESHOST_NEWS, timeout = 60)

# s = Search(using = es, index = 'langgar')

# for h in s.filter('range', timestamp={"lte": "2015-08-04"}).query("multi_match", query='indonesia', fields=['title', 'content']).params(size=150).execute().hits:
# 	print h.timestamp if 'timestamp' in h else ''

