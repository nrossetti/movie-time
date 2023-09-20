from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_models import MovieNight, MovieEvent, Movie

class DBManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def add_movie_night(self, title, description, status=0, current_movie_index=0):
        session = self.Session()
        new_movie_night = MovieNight(title=title, description=description, status=status, current_movie_index=current_movie_index)
        session.add(new_movie_night)
        session.commit()
        session.close()

    def add_movie_event(self, movie_night_id, movie_id, start_time, discord_id=None):
        session = self.Session()
        new_movie_event = MovieEvent(movie_night_id=movie_night_id, movie_id=movie_id, start_time=start_time, discord_id=discord_id)
        session.add(new_movie_event)
        session.commit()
        session.close()

    def add_movie(self, name, year, director, image_url, backdrop_url, runtime, budget, revenue, overview, release_date, url):
        session = self.Session()
        new_movie = Movie(
            name=name,
            year=year,
            director=director,
            image_url=image_url,
            backdrop_url=backdrop_url,
            runtime=runtime,
            budget=budget,
            revenue=revenue,
            overview=overview,
            release_date=release_date,
            url=url 
        )
        session.add(new_movie)
        session.commit()
        session.close()

    def get_movie_nights(self):
        session = self.Session()
        movie_nights = session.query(MovieNight).all()
        session.close()
        return movie_nights

    def get_movie_events(self, movie_night_id):
        session = self.Session()
        movie_events = session.query(MovieEvent).filter_by(movie_night_id=movie_night_id).all()
        session.close()
        return movie_events

    def get_movie(self, movie_id):
        session = self.Session()
        movie = session.query(Movie).filter_by(id=movie_id).first()
        session.close()
        return movie