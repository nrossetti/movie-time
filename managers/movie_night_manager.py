from database.db_models import MovieNight
from sqlalchemy.orm import Session

class MovieNightManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_movie_night(self, title, description, start_time = None):
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
    
    def get_most_recent_movie_night_id(self):
        most_recent = self.db_session.query(MovieNight).order_by(MovieNight.id.desc()).first()
        return most_recent.id if most_recent else None
        
    def get_movie_night(self, movie_night_id):
        try:
            movie_night = self.db_session.query(MovieNight).filter(MovieNight.id == movie_night_id).first()
            if movie_night:
                return movie_night
            else:
                raise ValueError(f"No Movie Night found with ID: {movie_night_id}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_movie_night_details(self, movie_night_id):
        movie_night = self.find_movie_night_by_id(movie_night_id)
        if not movie_night:
            return "Movie Night not found."
        
        details = {
            "title": movie_night.title, 
            "description": movie_night.description,
            "events": [
                {"event_id": event.id, "movie_name": event.movie.name, "start_time": event.start_time}
                for event in movie_night.events
            ]
        }
        return details
    
    def get_current_movie_event(self, movie_night_id):
        movie_night = self.find_movie_night_by_id(movie_night_id)
        if not movie_night or not movie_night.events:
            return None

        if 0 <= movie_night.current_movie_index < len(movie_night.events):
            return movie_night.events[movie_night.current_movie_index]
        return None