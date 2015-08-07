from os.path import abspath, isfile
import sys
sys.path.append(abspath(''))

import database.dbresult as dbr

def getclassified(kelas= '', size = 10, offset = 0):
  s = dbr.get_search_instance('LEARN', enc = False).params(size = size, from_ = offset)
  return s.execute().hits

print getclassified(kelas= 'haha')