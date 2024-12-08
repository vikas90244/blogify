from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLACHAMY_DATABASE_URL= "sqlite:///./blog.db"
engine = create_engine(SQLACHAMY_DATABASE_URL, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)


Base = declarative_base()



def get_db():
    db = SessionLocal()

    try:
        yield db
        # yield lets route use the db, like it will return db for use of create
        #execute code after it when create will be finished
    finally:
        db.close()