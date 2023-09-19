import unittest
from services.movie_scraper import MovieScraper
from utils.secret_manager import SecretManager

class TestMovieScraper(unittest.TestCase):

    def setUp(self):
        secrets = SecretManager().load_secrets()
        self.movie_scraper = MovieScraper(secrets['api_key'])

    def test_get_movie_details_from_url(self):
        url = 'https://letterboxd.com/film/national-treasure/'
        details = self.movie_scraper.get_movie_details_from_url(url)
        self.assertIsNotNone(details)

if __name__ == '__main__':
    unittest.main()