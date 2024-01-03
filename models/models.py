from base import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    alias = Column(String, nullable=True, index=True)
    abbrv = Column(String, nullable=True, index=True)
    founded = Column(Integer, nullable=True)
    owner = Column(String, nullable=True)
    general_manager = Column(String, nullable=True)
    president = Column(String, nullable=True)
    primary_color = Column(String, nullable=True)
    offensive_coordinator = Column(String, nullable=True)
    defensive_coordinator = Column(String, nullable=True)
    championships_won = Column(Integer, nullable=True)
    championship_seasons = Column(String, nullable=True)
    conference_titles = Column(Integer, nullable=True)
    division_titles = Column(Integer, nullable=True)
    playoff_appearances = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __str__(self):
        return self.name

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    active_club_id = Column(Integer, ForeignKey('clubs.id'), nullable=True)
    name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    college = Column(String, nullable=True)
    experience = Column(Integer, nullable=True)
    age = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(String, nullable=True)
    position = Column(String, nullable=True)
    status = Column(String, nullable=True)
    headshot_url = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    active_team = relationship('Club', foreign_keys=[active_club_id])

class History(Base):
    __tablename__ = "player_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    name = Column(String, index=True, nullable=True)
    season = Column(String, nullable=True)
    club_id = Column(Integer, ForeignKey('clubs.id'))
    started = Column(Boolean)
    played = Column(Boolean)
    position = Column(String, nullable=True)
    team = Column(String, nullable=True)
    opponent_rank = Column(String, nullable=True)
    offensive_plays = Column(Integer, nullable=True)
    defensive_plays = Column(Integer, nullable=True)
    offensive_team_plays = Column(Integer, nullable=True)
    defensive_team_plays = Column(Integer, nullable=True)
    offense_play_time_percentage = Column(Float, nullable=True)
    defense_play_time_percentage = Column(Float, nullable=True)
    week = Column(Integer, nullable=True)
    game_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    player = relationship("Player")
    club = relationship("Club")

class Salary(Base):
    __tablename__ = "player_salary"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    season = Column(Integer, nullable=True)
    active_club_id = Column(Integer, ForeignKey('clubs.id'))
    contract_duration = Column(Integer, nullable=True)
    salary_amount =  Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    player = relationship("Player")
    club = relationship("Club")

class Transactions(Base):
    __tablename__ = "player_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    type = Column(String, nullable=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    position = Column(String, nullable=True)
    date = Column(DateTime, nullable=True, index=True)
    sending_club_id = Column(Integer, ForeignKey('clubs.id'))
    receiving_club_id = Column(Integer, ForeignKey('clubs.id'))
    transaction_year = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    player = relationship("Player")
    sending_club = relationship("Club", foreign_keys=[sending_club_id])
    receiving_club = relationship("Club", foreign_keys=[receiving_club_id])
