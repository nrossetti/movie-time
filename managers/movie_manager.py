from database.db_models import Movie
from sqlalchemy.orm import Session

class MovieManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_movie(self, movie_details):
        new_movie = Movie(
            name=movie_details['name'],
            year=int(movie_details['year']),
            director=movie_details['director'],
            image_url=movie_details['image_url'],
            backdrop_url=movie_details['backdrop_url'],
            runtime=int(movie_details['runtime']),
            budget=int(movie_details['budget']),
            revenue=int(movie_details['revenue']),
            overview=movie_details['overview'],
            release_date=movie_details['release_date']
        )
        self.db_session.add(new_movie)
        self.db_session.commit()
        return new_movie.id
