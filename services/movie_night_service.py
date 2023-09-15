from services.movie_scraper import MovieScraper
from datetime import timedelta

class MovieNightService:
    def __init__(self, movie_night_manager, movie_manager, movie_event_manager, movie_scraper: MovieScraper):
        self.movie_night_manager = movie_night_manager
        self.movie_manager = movie_manager
        self.movie_event_manager = movie_event_manager
        self.movie_scraper = movie_scraper

    def round_to_next_quarter_hour(self, time):
        minutes_to_next_quarter_hour = 15 - time.minute % 15
        return time + timedelta(minutes=minutes_to_next_quarter_hour)

    def add_movie_to_movie_night(self, movie_night_id, movie_url, api_key):
        movie_details = self.movie_scraper.get_movie_details_from_url(movie_url)

        if not movie_details:
            return "Failed to get movie details."

        existing_movie = self.movie_manager.find_movie_by_name_and_year(movie_details['name'], movie_details['year'])
        if existing_movie:
            movie_id = existing_movie.id
        else:
            movie_id = self.movie_manager.save_movie(movie_details)

        movie_night = self.movie_night_manager.find_movie_night_by_id(movie_night_id)

        if not movie_night:
            return "Movie Night not found"

        last_movie_event = self.movie_event_manager.find_last_movie_event_by_movie_night_id(movie_night_id)

        if last_movie_event:
            last_movie = self.movie_manager.find_movie_by_id(last_movie_event.movie_id)
            if last_movie:
                last_movie_end_time = last_movie_event.start_time + timedelta(minutes=last_movie.runtime)
            else:
                last_movie_end_time = movie_night.start_time
        else:
            last_movie_end_time = movie_night.start_time

        if last_movie_end_time is not None:  # Add this line to check for None
            new_start_time = self.round_to_next_quarter_hour(last_movie_end_time)
        else:
            return "Error: Cannot calculate new start time."

        new_movie_event_id = self.movie_event_manager.create_movie_event(movie_night_id, movie_id, new_start_time)

        return new_movie_event_id
    
    