import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

conn_string = f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWD']}@{os.environ['MYSQL_URL']}/{os.environ['MYSQL_DATABASE']}"
engine = create_engine(conn_string)
DBSession = sessionmaker(bind=engine)