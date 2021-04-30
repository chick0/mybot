from configparser import ConfigParser

conf = ConfigParser()
conf.read("alembic.ini")

URL = conf['alembic']['sqlalchemy.url']


del ConfigParser, conf
