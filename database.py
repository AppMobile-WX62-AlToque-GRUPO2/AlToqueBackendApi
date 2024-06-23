from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

MYSQL_USER = 'root'
MYSQL_PASSWORD = 'SwpDLuFhUzWYnMMUdOcJZiJiBJXcKGBA'
MYSQL_HOST = 'monorail.proxy.rlwy.net'
MYSQL_PORT = '23253'
MYSQL_DATABASE = 'railway'

URL_DATABASE = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
