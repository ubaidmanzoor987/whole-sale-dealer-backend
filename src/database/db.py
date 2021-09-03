from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'postgresql+psycopg2://admin:admin123@localhost/whole_sale_management'
# DATABASE_URI = 'postgresql+psycopg2://glaxiUser:webdir123R$@glaxi-db.c6cd13oyadwd.us-east-1.rds.amazonaws.com/wd-db'

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
        self.engine = create_engine(DATABASE_URI)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=True,
                                                      bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()
        from src.models import ShopKeepers

        self.Base.metadata.create_all(bind=self.engine)

