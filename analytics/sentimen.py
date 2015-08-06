import sys
import database.dbresult as dbr

from os.path import abspath

sys.path.append(abspath(''))

def getclassified(class = '', size = 10, offset = 0):
  print class
  s = dbr.get_search_instance('LEARN', enc = False).params(size = size, from_ = offset)
  return s.execute().hits