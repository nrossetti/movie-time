from datetime import datetime
from database.database import SessionLocal
from managers.movie_manager import MovieManager
from managers.movie_night_manager import MovieNightManager
from managers.movie_event_manager import MovieEventManager
from services.movie_night_service import MovieNightService
from services.movie_scraper import MovieScraper
from utils.secret_manager import SecretManager

secrets = SecretManager().load_secrets()
api_key = secrets['api_key']

movie_scraper = MovieScraper(api_key)

db_session = SessionLocal()
movie_manager = MovieManager(db_session)
movie_night_manager = MovieNightManager(db_session)
movie_event_manager = MovieEventManager(db_session)

movie_night_service = MovieNightService(movie_night_manager, movie_manager, movie_event_manager, movie_scraper)

print("Simulating /createmovienight command...")
title = "Comedy Night"
description = "A night full of laughter."
time = datetime.now()
movie_night_id = movie_night_manager.create_movie_night(title, description, time)
print(f"Created Movie Night with ID: {movie_night_id}")

print("Simulating /addmovie or /addmovies command...")
movie_urls = [
    "https://letterboxd.com/film/national-treasure/",
    "https://letterboxd.com/film/the-retirement-plan/",
    "https://letterboxd.com/film/dream-scenario/",
]

for url in movie_urls:
    print(f"Adding movie from URL: {url}")
    movie_event_id = movie_night_service.add_movie_to_movie_night(movie_night_id, url, api_key)
    if movie_event_id:
        print(f"Added Movie to Movie Night. Movie Event ID is: {movie_event_id}")
    else:
        print("Failed to add movie.")

print("End of Script.")
