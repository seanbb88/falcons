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
    
    active_team = relationship('Club', foreign_keys=[active_club_id])
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __str__(self):
        return self.name

class History(Base):
    __tablename__ = "player_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    name = Column(String, index=True, nullable=True)
    season = Column(String, index=True, nullable=True)
    club_id = Column(Integer, ForeignKey('clubs.id'))
    started = Column(Boolean)
    played = Column(Boolean)
    position = Column(String, index=True, nullable=True)
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
    
    player = relationship("Player")
    club = relationship("Club")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class Salary(Base):
    __tablename__ = "player_salary"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=True)
    year_signed = Column(String, nullable=True)
    team = Column(String, nullable=True)
    average_per_year = Column(Integer, nullable=True)
    total_value =  Column(Integer, nullable=True)
    guaranteed =  Column(Integer, nullable=True)
    position = Column(String)
    
    player = relationship("Player")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

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
    
    player = relationship("Player")
    sending_club = relationship("Club", foreign_keys=[sending_club_id])
    receiving_club = relationship("Club", foreign_keys=[receiving_club_id])
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class PositionAggregation(Base):
    __tablename__ = "position_aggregations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    position = Column(String, nullable=False)
    total_team_plays = Column(Integer, nullable=False)
    total_offensive_team_plays = Column(Integer, nullable=False)
    total_defensive_team_plays = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    

class ClubAggregation(Base):
    __tablename__ = "club_aggregations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    club_name = Column(String, nullable=False)
    total_team_plays = Column(Integer, nullable=False)
    total_offensive_team_plays = Column(Integer, nullable=False)
    total_defensive_team_plays = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
class SeasonAggregation(Base):
    __tablename__ = "season_aggregations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(String, nullable=False)
    total_team_plays = Column(Integer, nullable=False)
    total_offensive_team_plays = Column(Integer, nullable=False)
    total_defensive_team_plays = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
class PlayerRankingSeasonAggregation(Base):
    __tablename__ = "player_ranking_season_aggregation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    player_id = Column(Integer, ForeignKey('players.id'))
    season = Column(String)
    defense_plays_percentile = Column(Float, nullable=True)
    offense_plays_percentile = Column(Float, nullable=True)

    player = relationship("Player")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
class PlayerRankingPositionAggregation(Base):
    __tablename__ = "player_ranking_position_aggregation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    player_id = Column(Integer, ForeignKey('players.id'))
    position = Column(String)
    defense_plays_percentile = Column(Float, nullable=True)
    offense_plays_percentile = Column(Float, nullable=True)
    
    player = relationship("Player")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
class PlayerRankingClubAggregation(Base):
    __tablename__ = "player_ranking_club_aggregation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    player_id = Column(Integer, ForeignKey('players.id'))
    club = Column(String)
    defense_plays_percentile = Column(Float, nullable=True)
    offense_plays_percentile = Column(Float, nullable=True)
    
    player = relationship("Player")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
