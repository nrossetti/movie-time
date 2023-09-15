from database.db_models import MovieEvent, MovieNight, Movie
from sqlalchemy.orm import Session
from sqlalchemy import desc

class MovieEventManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_movie_event(self, movie_night_id, movie_id, start_time):
        new_movie_event = MovieEvent(movie_night_id=movie_night_id, movie_id=movie_id, start_time=start_time)
        self.db_session.add(new_movie_event)
        self.db_session.commit()
        return new_movie_event.id

    def update_movie_event(self, movie_event_id, movie_night_id=None, movie_id=None, start_time=None):
        movie_event = self.db_session.query(MovieEvent).filter_by(id=movie_event_id).first()
        if not movie_event:
            return "Movie Event not found"

        if movie_night_id:
            movie_event.movie_night_id = movie_night_id
        if movie_id:
            movie_event.movie_id = movie_id
        if start_time:
            movie_event.start_time = start_time

        self.db_session.commit()
        return movie_event.id

    def delete_movie_event(self, movie_event_id):
        movie_event = self.db_session.query(MovieEvent).filter_by(id=movie_event_id).first()
        if not movie_event:
            return "Movie Event not found"

        self.db_session.delete(movie_event)
        self.db_session.commit()
        return "Deleted successfully"

    def list_all_movie_events(self):
        return self.db_session.query(MovieEvent).all()

    def find_movie_event_by_id(self, movie_event_id):
        return self.db_session.query(MovieEvent).filter_by(id=movie_event_id).first()
    
    def find_last_movie_event_by_movie_night_id(self, movie_night_id):
        result = self.db_session.query(MovieEvent)\
            .filter_by(movie_night_id=movie_night_id)\
            .order_by(desc(MovieEvent.start_time))\
            .first()
        return result