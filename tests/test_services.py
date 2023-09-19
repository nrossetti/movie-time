import unittest
from datetime import datetime
from database.database import SessionLocal
from managers.movie_manager import MovieManager
from managers.movie_night_manager import MovieNightManager
from managers.movie_event_manager import MovieEventManager
from services.movie_night_service import MovieNightService
from services.movie_scraper import MovieScraper
from utils.secret_manager import SecretManager

class TestMovieNightService(unittest.TestCase):

    import unittest
from datetime import datetime
from database.database import SessionLocal
from managers.movie_manager import MovieManager
from managers.movie_night_manager import MovieNightManager
from managers.movie_event_manager import MovieEventManager
from services.movie_night_service import MovieNightService
from services.movie_scraper import MovieScraper
from utils.secret_manager import SecretManager

class TestMovieNightService(unittest.TestCase):

    def setUp(self):
        self.db_session = SessionLocal()
        self.db_session.begin_nested()
        self.movie_night_manager = MovieNightManager(self.db_session)
        self.movie_manager = MovieManager(self.db_session)
        self.movie_event_manager = MovieEventManager(self.db_session)
        
        self.secrets = SecretManager().load_secrets()
        self.movie_scraper = MovieScraper(self.secrets['api_key'])  # Initialize with API key
        
        self.movie_night_service = MovieNightService(
            self.movie_night_manager, 
            self.movie_manager, 
            self.movie_event_manager,
            self.movie_scraper  # Pass initialized MovieScraper
        )
        

    def test_add_movie_to_movie_night_successful(self):
        movie_night_id = self.movie_night_manager.create_movie_night("Movie Night 1", "Description 1", start_time=datetime.now())
        movie_url = "https://letterboxd.com/film/national-treasure/"

        new_movie_event_id = self.movie_night_service.add_movie_to_movie_night(
            movie_night_id, 
            movie_url, 
            self.secrets['api_key']
        )
        
        self.assertIsNotNone(new_movie_event_id, "Failed to add movie to movie night.")

    def tearDown(self):
            self.db_session.close()   

if __name__ == '__main__':
    unittest.main()
