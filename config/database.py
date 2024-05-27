from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# MySQL database configuration
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'SwpDLuFhUzWYnMMUdOcJZiJiBJXcKGBA'
MYSQL_HOST = 'monorail.proxy.rlwy.net'
MYSQL_PORT = '23253'
MYSQL_DATABASE = 'railway'

# Database connection URL
#mysql://root:SwpDLuFhUzWYnMMUdOcJZiJiBJXcKGBA@monorail.proxy.rlwy.net:23253/railway
URL_DATABASE = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'

# Create the database engine
engine = create_engine(URL_DATABASE)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()


# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()