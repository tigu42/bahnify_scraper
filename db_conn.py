import mariadb
import sys
import message_logger
import time

class db_connection():
    def __init__(self):
        start_time = time.time()
        timeout = 180
        
        while True:
            try:
                self.conn = mariadb.connect(
                user="root",
                password="PASSWORD",
                host="localhost",
                port=3306,
                database="bahnify"
                )
                break
            except mariadb.Error as e:
                message_logger.log_normal(f"Error connecting to MariaDB Platform: {e}")
                message_logger.log_normal("Database Error, retrying in 5 seconds")
                time.sleep(5)
                if time.time() - start_time > timeout:
                    message_logger.log_critical("Database connection failed, exiting")
                    sys.exit(1)
    
    def execute_query(self, query: str, params = ()):
        cur = self.conn.cursor()
        cur.execute(query.lower(), params)
        return cur.fetchall()

    def execute_insert(self, query: str, params = ()):
        cur = self.conn.cursor()
        cur.execute(query.lower(), params)
        self.conn.commit()
        return cur.lastrowid
    
