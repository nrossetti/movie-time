import unittest
from datetime import datetime
from database.database import SessionLocal
from managers.movie_manager import MovieManager
from managers.movie_night_manager import MovieNightManager
from managers.movie_event_manager import MovieEventManager

class TestMovieEventManager(unittest.TestCase):

    def setUp(self):
        self.db_session = SessionLocal()
        self.movie_event_manager = MovieEventManager(self.db_session)
        self.movie_manager = MovieManager(self.db_session)
        self.movie_night_manager = MovieNightManager(self.db_session)

        self.movie_details = {
            'name': 'National Treasure',
            'year': 2004,
            'director': 'Jon Turteltaub',
            'image_url': 'some_url',
            'backdrop_url': 'some_backdrop_url',
            'runtime': 131,
            'budget': 100000000,
            'revenue': 347512318,
            'overview': 'Modern treasure hunters, led by archaeologist Ben Gates, search for a chest of riches.',
            'release_date': '2004-11-19'
        }

        existing_movie = self.movie_manager.find_movie_by_name_and_year(self.movie_details['name'], self.movie_details['year'])
        self.movie_id = existing_movie.id if existing_movie else self.movie_manager.save_movie(self.movie_details)

    def test_save_movie(self):
        new_movie_id = self.movie_manager.save_movie(self.movie_details)
        self.assertEqual(new_movie_id, self.movie_id)

class TestMovieNightManager(unittest.TestCase):
    
    def setUp(self):
        self.db_session = SessionLocal()
        self.manager = MovieNightManager(self.db_session)

    def test_create_movie_night(self):
        new_movie_night_id = self.manager.create_movie_night("Comedy Night", "A night full of laughter.", start_time=datetime.now())
        self.assertIsNotNone(new_movie_night_id)

    def test_update_movie_night(self):
        new_movie_night_id = self.manager.create_movie_night("Comedy Night", "A night full of laughter.", start_time=datetime.now())
        updated_movie_night_id = self.manager.update_movie_night(new_movie_night_id, title="Action Night")
        self.assertEqual(new_movie_night_id, updated_movie_night_id)

    def test_delete_movie_night(self):
        new_movie_night_id = self.manager.create_movie_night("Comedy Night", "A night full of laughter.", start_time=datetime.now())
        result = self.manager.delete_movie_night(new_movie_night_id)
        self.assertEqual(result, "Deleted successfully")

    def test_list_all_movie_nights(self):
        all_movie_nights = self.manager.list_all_movie_nights()
        self.assertIsInstance(all_movie_nights, list)

    def test_find_movie_night_by_id(self):
        new_movie_night_id = self.manager.create_movie_night("Comedy Night", "A night full of laughter.", start_time=datetime.now())
        movie_night = self.manager.find_movie_night_by_id(new_movie_night_id)
        self.assertIsNotNone(movie_night)

    def tearDown(self):
        self.db_session.close()

class TestMovieEventManager(unittest.TestCase):

    def setUp(self):
        self.db_session = SessionLocal()
        self.movie_event_manager = MovieEventManager(self.db_session)
        self.movie_manager = MovieManager(self.db_session)
        self.movie_night_manager = MovieNightManager(self.db_session)

        self.movie_details = {
            'name': 'National Treasure',
            'year': 2004,
            'director': 'Jon Turteltaub',
            'image_url': 'some_url',
            'backdrop_url': 'some_backdrop_url',
            'runtime': 131,
            'budget': 100000000,
            'revenue': 347512318,
            'overview': 'Modern treasure hunters, led by archaeologist Ben Gates, search for a chest of riches.',
            'release_date': '2004-11-19'
        }

        existing_movie = self.movie_manager.find_movie_by_name_and_year('National Treasure', 2004)
        self.existing_movie = existing_movie if existing_movie else self.movie_manager.save_movie(self.movie_details)
        
        existing_movie_night = self.movie_night_manager.find_movie_night_by_title("Comedy Night")
        self.existing_movie_night = existing_movie_night if existing_movie_night else self.movie_night_manager.create_movie_night("Comedy Night", "A night full of laughter.", datetime.now())

        if isinstance(self.existing_movie, int):
            self.existing_movie = self.movie_manager.find_movie_by_id(self.existing_movie)
            
        if isinstance(self.existing_movie_night, int):
            self.existing_movie_night = self.movie_night_manager.find_movie_night_by_id(self.existing_movie_night)

        self.existing_movie_event_id = self.movie_event_manager.create_movie_event(self.existing_movie_night.id, self.existing_movie.id, datetime.now())

    def test_create_movie_event(self):
        new_movie_event_id = self.movie_event_manager.create_movie_event(self.existing_movie_night.id, self.existing_movie.id, datetime.now())
        self.assertIsNotNone(new_movie_event_id)

    def test_update_movie_event(self):
        updated_movie_event_id = self.movie_event_manager.update_movie_event(self.existing_movie_event_id, start_time=datetime.now())
        self.assertEqual(self.existing_movie_event_id, updated_movie_event_id)

    def test_delete_movie_event(self):
        delete_status = self.movie_event_manager.delete_movie_event(self.existing_movie_event_id)
        self.assertEqual(delete_status, "Deleted successfully")

if __name__ == '__main__':
    unittest.main()