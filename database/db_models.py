from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MovieNight(Base):
    __tablename__ = 'movie_nights'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

    events = relationship("MovieEvent", back_populates="movie_night")

class MovieEvent(Base):
    __tablename__ = 'movie_events'

    id = Column(Integer, primary_key=True)
    movie_night_id = Column(Integer, ForeignKey('movie_nights.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    start_time = Column(DateTime)

    movie_night = relationship("MovieNight", back_populates="events")
    movie = relationship("Movie", back_populates="events")

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    director = Column(String)
    image_url = Column(String)
    backdrop_url = Column(String)
    runtime = Column(Integer)
    budget = Column(Integer)
    revenue = Column(Integer)
    overview = Column(String)
    release_date = Column(String)

    events = relationship("MovieEvent", back_populates="movie")

engine = create_engine('sqlite:///movie_nights.db')
Base.metadata.create_all(engine)
