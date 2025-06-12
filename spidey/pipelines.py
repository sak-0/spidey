# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from mysql.connector import Error

class SpideyPipeline:
    def __init__(self):
        self.conn = None
        self.cur = None

    def open_Spider(self, spider):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='spidey',
                password='pretti-damn-conphident',
                database='spidey_db'
            )
            self.cur = self.conn.cursor()
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS reps (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    rep_id VARCHAR(255),
                    phone VARCHAR(50),
                    email VARCHAR(255)
                )"""
            )
        except Error as e:
            print(f"error connecting to MySQL: {e}")

    def process_item(self, item, spider):
        try:
            self.cur.execute(
                "INSERT INTO reps (name, rep_id, phone, email) VALUES (%s, %s, %s, %s)",
                (
                    item.get('name'), 
                    item.get('rep_id'), 
                    item.get('phone'), 
                    item.get('email')
                )
            )
            self.conn.commit()
        except Error as e:
            spider.logger.error(f"failed to insert item into db: {e}")
        return item

    def close_spider(self, spider):
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            spider.logger.error(f"[db error] Error during db cleanup: {e}")