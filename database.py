from base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from models import Club, Player, Transactions, History, Salary
from utils.loaders import print_progress_dots


db_url = "postgresql://seanbrown:password@localhost/falcons"

def initialize_database():
    print("INITIALIZING DATABASE (IF NEEDED)")
    print_progress_dots(12)
    if not database_exists(db_url):
        create_database(db_url) 
    Base.metadata.create_all(bind=engine)
    

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

