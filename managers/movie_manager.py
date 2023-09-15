from database.db_models import Movie
from sqlalchemy.orm import Session

class MovieManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_movie(self, movie_details):
        existing_movie = self.db_session.query(Movie).filter_by(
            name=movie_details['name'],
            year=int(movie_details['year'])
        ).first()

        if existing_movie:
            return existing_movie.id

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
    
    def find_movie_by_name_and_year(self, name, year):
        return self.db_session.query(Movie).filter_by(name=name, year=year).first()

    def find_movie_by_id(self, movie_id):
        return self.db_session.query(Movie).filter_by(id=movie_id).first()