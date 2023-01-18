from dotenv import load_dotenv
import os

class Config():
    load_dotenv()
    SECRET_KEY = os.environ['SECRET_KEY']
    MYSQL_URL = f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWD']}@localhost/{os.environ['MYSQL_DATABASE']}"
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWD']}@localhost/{os.environ['MYSQL_DATABASE']}"


