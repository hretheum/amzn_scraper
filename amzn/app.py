from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path= Path('../') / '.env'
load_dotenv(dotenv_path=env_path)


class App:
  __conf = {
    "mysql_url": os.getenv("MYSQL_URL"),
    "username": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWD"),
    "MYSQL_PORT": 3306,
    "MYSQL_DATABASE": 'amzn',
    "scraper_api_key": os.getenv("SCRAPER_API_KEY")
  }
  __setters = ["username", "password"]

  @staticmethod
  def config(name):
    return App.__conf[name]

  @staticmethod
  def set(name, value):
    if name in App.__setters:
      App.__conf[name] = value
    else:
      raise NameError("Name not accepted in set() method")