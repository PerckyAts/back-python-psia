import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
dotenv.load_dotenv()

db_user = os.getenv("DB_USER")
db_pswd = os.getenv("DB_PSWD")
db_host = os.getenv("DB_HOST", default='127.0.0.1')
db_port = os.getenv("DB_PORT", default=5432)
db_name = os.getenv("DB_NAME")
db_url = f"mariadb://{db_user}:{db_pswd}@{db_host}/{db_name}"



DATABASE_URL = f"postgresql+psycopg2://{str(db_user)}:{str(db_pswd)}@{str(db_host)}/{str(db_name)}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#création d'une session sqlalchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# A retirer si alembic
def init_db():
    Base.metadata.create_all(engine)