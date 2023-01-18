import MySQLdb
from amzn.app import App
from itertools import chain
class MySqlAmznPipeline:

    def __init__(self):
        self.conn = MySQLdb.connect(
            host=App.config("mysql_url"),
            port=App.config("MYSQL_PORT"),
            user=App.config("username"),
            password=App.config("password"),
            database=App.config("MYSQL_DATABASE")
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS offers(
            asin text,
            price text,
            timestamp text
            )
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS products(
            asin text,
            title text)
        """)


    def process_item(self, item, spider):

        self.cur.execute("""SELECT EXISTS (SELECT * FROM products WHERE asin=%s)""", (item['asin'],))

        product = self.cur.fetchone()[0]

        self.cur.execute("SELECT EXISTS (SELECT * FROM offers WHERE asin=%s AND timestamp=%s)", (item['asin'], item['timestamp']))
        offer = self.cur.fetchone()[0]

        if not product:
            self.cur.execute("INSERT INTO products (asin, title) values (%s, %s)", (item['asin'], item['title']))
            self.cur.execute("INSERT INTO offers (asin, title,   price, timestamp) values (%s, %s, %s, %s)", (item['asin'], item['title'], item['price'], item['timestamp']))
            self.cur.execute("INSERT INTO q2o (queryID, offerID) values (%s, %s)", (item['queryID'], self.cur.lastrowid))

        else:
            if not offer:
                self.cur.execute("INSERT INTO offers (asin, title, price, timestamp) values (%s, %s, %s, %s)", (item['asin'], item['title'], item['price'], item['timestamp']))
                self.cur.execute("INSERT INTO q2o (queryID, offerID) values (%s, %s)", (item['queryID'], self.cur.lastrowid))

        self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

class AmznItemPipeline:

    def __init__(self):
        self.conn = MySQLdb.connect(
            host=App.config("mysql_url"),
            port=App.config("MYSQL_PORT"),
            user=App.config("username"),
            password=App.config("password"),
            database=App.config("MYSQL_DATABASE")
        )

        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        self.cur.execute("SELECT EXISTS (SELECT * FROM offers WHERE asin=%s AND timestamp=%s)",
                         (item['asin'], item['timestamp']))
        offer = self.cur.fetchone()[0]

        if not offer:
            self.cur.execute("INSERT INTO offers (asin, price, timestamp) values (%s, %s, %s)",
                             (item['asin'], item['price'], item['timestamp']))
            self.cur.execute("INSERT INTO q2o (queryID, offerID, visible) values (%s, %s, True)",
                             (item['queryID'], self.cur.lastrowid))

        self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()