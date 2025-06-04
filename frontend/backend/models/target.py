import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class TargetModel:
    def __init__(self, url, status=None, latency=None, last_checked=None, id=None):
        self.id = id
        self.url = url
        self.status = status
        self.latency = latency
        self.last_checked = last_checked

    def get_connection(self):
        return mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'mininetumo')
        )

    def save(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute("""
                    UPDATE targets
                    SET url=%s, status=%s, latency=%s, last_checked=%s
                    WHERE id=%s
                """, (self.url, self.status, self.latency, self.last_checked, self.id))
            else:
                cursor.execute("""
                    INSERT INTO targets (url, status, latency, last_checked)
                    VALUES (%s, %s, %s, %s)
                """, (self.url, self.status, self.latency, self.last_checked))
                self.id = cursor.lastrowid
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'status': self.status,
            'latency': self.latency,
            'last_checked': self.last_checked.isoformat() if self.last_checked else None
        }

    @classmethod
    def get_all(cls):
        conn = cls().get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, url, status, latency, last_checked FROM targets")
            results = cursor.fetchall()
            return [cls(id=row[0], url=row[1], status=row[2], latency=row[3], last_checked=row[4]) for row in results]
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_by_id(cls, target_id):
        conn = cls().get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, url, status, latency, last_checked FROM targets WHERE id = %s", (target_id,))
            row = cursor.fetchone()
            if row:
                return cls(id=row[0], url=row[1], status=row[2], latency=row[3], last_checked=row[4])
            return None
        finally:
            cursor.close()
            conn.close()

# Create table
conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', ''),
    database=os.getenv('MYSQL_DATABASE', 'mininetumo')
)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS targets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url VARCHAR(255) NOT NULL,
        status VARCHAR(50),
        latency FLOAT,
        last_checked DATETIME
    )
""")
conn.commit()
cursor.close()
conn.close()
