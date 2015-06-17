from sqlalchemy import create_engine, Column, String
engine = create_engine('mysql:///:memory:', echo=True)

class Keyword():

  __tablename__ = 'streamings'
  keyword = Column(String(64), primary_key = True, index = True)

  """Representing a keyword, just keyword!"""
  def __init__(self, key):
    keyword = key
