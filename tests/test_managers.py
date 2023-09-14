import unittest
from database.database import SessionLocal
from managers.movie_manager import MovieManager

class TestMovieManager(unittest.TestCase):

    def setUp(self):
        self.db_session = SessionLocal()
        self.movie_manager = MovieManager(self.db_session)

    def test_save_movie(self):
        movie_details = {
            'name': 'Inception',
            'year': 2010,
            'director': 'Christopher Nolan',
            'image_url': 'some_url',
            'backdrop_url': 'some_backdrop_url',
            'runtime': 120,
            'budget': 200000000,
            'revenue': 800000000,
            'overview': 'A mind-bending thriller',
            'release_date': '2010-07-16'
        }
        new_movie_id = self.movie_manager.save_movie(movie_details)
        self.assertIsNotNone(new_movie_id)

if __name__ == '__main__':
    unittest.main()