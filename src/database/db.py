from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values
config = dotenv_values(".env")
DATABASE_URI = config['DB_URI']

class Session:
    session = None
    @staticmethod
    def create_session():
        Session.session = Session()
        Session.session.init_db()

    def destroy_session(self):
        self.db_session.close()
        self.engine.dispose()

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.db_session

    def get_base(self):
        return self.Base

    def init_db(self):
        self.engine = create_engine(DATABASE_URI, pool_size=20, max_overflow=0)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=True,
                                                      bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()
        from src.models import User, Brands, Products, Orders, ExpoPushTokens
        self.Base.metadata.create_all(bind=self.engine)

