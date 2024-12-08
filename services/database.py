import os
import time
import traceback

import psycopg2
from psycopg2.extras import RealDictCursor

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DatabaseConfig


engine = create_engine(DatabaseConfig.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PgDriver:

    """ Контекстный менеджер для работы с БД прямыми SQL запросами. """

    def __init__(self):
        self._dsn = DatabaseConfig.DATABASE_URL

    def __enter__(self):
        self.conn = None
        count = 0
        while not self.conn:
            try:
                self.conn = psycopg2.connect(self._dsn, cursor_factory=RealDictCursor)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                print('except ERROR CONNECT DB!')
                count += 1

                time.sleep(10)
                try:
                    self.conn.close()
                except Exception as e:
                    print('close error')
                    print(e)
                    print(traceback.format_exc())
                continue

            if count > 20:
                print(self.conn)
                raise ConnectionError('ERROR CONNECT DB!')

        self.curr = self.conn.cursor()

        return self.curr

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.curr.close()
        self.conn.close()
