import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean, Table
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    public_id = Column(Integer, unique=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'[jusek id: {self.id} | username: {self.username}]'

class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    asin = Column(String(255))
    price = Column(String(255))
    timestamp = Column(String(255))
    title = Column(String(255))
    queries = relationship(
        "Query",
        secondary="q2o",
        back_populates='offers'
    )

    def __repr__(self):
        return f'<Offer ||| id: {self.id}, {self.asin}, cena: {self.price}, data: {self.timestamp}, tytuł:  {self.title} >'


class Query(Base):
    __tablename__ = 'queries'
    id = Column(Integer, primary_key=True)
    query = Column(String(255))
    timestamp = Column(String(255))
    offers = relationship(
        "Offer",
        secondary="q2o",
        back_populates='queries'
    )

    def __repr__(self):
        return f'<Query {self.id} {self.query} {self.timestamp}  >'


q2o = Table(
    'q2o',
    Base.metadata,
    Column('queryID', Integer, ForeignKey(Query.id), primary_key=True),
    Column('offerID', Integer, ForeignKey(Offer.id), primary_key=True),
    Column('category', String(255)),
    Column('visible', Boolean, nullable=False, server_default='1')
)


class UserQueries(Base):
    __tablename__ = 'userqueries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, ForeignKey(User.id), primary_key=True)
    queryID = Column(Integer, ForeignKey(Query.id), primary_key=True)
    visible = Column(Boolean, default=True)


if __name__ == '__main__':
    load_dotenv()
    conn_string = f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWD']}@{os.environ['MYSQL_URL']}/{os.environ['MYSQL_DATABASE']}"
    engine = create_engine(conn_string)
    Base.metadata.create_all(engine)