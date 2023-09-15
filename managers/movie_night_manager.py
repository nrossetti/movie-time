from database.db_models import MovieNight
from sqlalchemy.orm import Session
from datetime import datetime

class MovieNightManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_movie_night(self, title, description, start_time: datetime = None):
        new_movie_night = MovieNight(title=title, description=description, start_time=start_time)
        self.db_session.add(new_movie_night)
        self.db_session.commit()
        return new_movie_night.id

    def update_movie_night(self, movie_night_id, title=None, description=None):
        movie_night = self.db_session.query(MovieNight).filter_by(id=movie_night_id).first()
        if not movie_night:
            return "Movie Night not found"

        if title:
            movie_night.title = title
        if description:
            movie_night.description = description

        self.db_session.commit()
        return movie_night.id

    def delete_movie_night(self, movie_night_id):
        movie_night = self.db_session.query(MovieNight).filter_by(id=movie_night_id).first()
        if not movie_night:
            return "Movie Night not found"

        self.db_session.delete(movie_night)
        self.db_session.commit()
        return "Deleted successfully"

    def list_all_movie_nights(self):
        return self.db_session.query(MovieNight).all()

    def find_movie_night_by_id(self, movie_night_id):
        return self.db_session.query(MovieNight).filter_by(id=movie_night_id).first()
        
    def find_movie_night_by_title(self, title):
        return self.db_session.query(MovieNight).filter_by(title=title).first()