from project.models import User, Offer, Query, q2o, UserQueries
from project.extensions import DBSession
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean, Table
from sqlalchemy.orm import declarative_base
import os

if __name__ == '__main__':
    load_dotenv()
    conn_string = f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWD']}@{os.environ['MYSQL_URL']}/{os.environ['MYSQL_DATABASE']}"
    engine = create_engine(conn_string)
    session = DBSession()
    admin = User(username=input('wprowadź email: '))
    admin.set_password(input('wprowadź hasło admina: '))
    session.add(admin)
    session.commit()