from base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from models import Club, Player, Transactions, History, Salary, PositionAggregation, ClubAggregation, SeasonAggregation, PlayerRankingSeasonAggregation, PlayerRankingPositionAggregation, PlayerRankingClubAggregation
from utils.loaders import print_progress_dots


local_connection_string = "postgresql://username:password@localhost/"
database = 'falcons'
full_connection_string = local_connection_string + database

def initialize_database():
    print("INITIALIZING DATABASE (IF NEEDED)")
    print_progress_dots(12)
    if not database_exists(full_connection_string):
        create_database(full_connection_string) 
    Base.metadata.create_all(bind=engine)
    

engine = create_engine(full_connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

