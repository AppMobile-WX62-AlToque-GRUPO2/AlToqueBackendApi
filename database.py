from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DB_HOST = "roundhouse.proxy.rlwy.net"
DB_USER = "root"
DB_PASSWORD = "GqxRyzzDxMgRCAsadwNhDefsnSQhkhvF"
DB_NAME = "railway"
DB_PORT = "57433"

URL_DATABASE = f'mysql+pymysql://{DB_HOST}:{DB_USER}@{DB_PASSWORD}:{DB_PORT}/{DB_NAME}'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
