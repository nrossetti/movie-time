from services.movie_scraper import MovieScraper
from bot_core.discord_events import DiscordEvents
from datetime import datetime, timedelta
from pytz import utc
from utils.image_util import download_image, convert_image_format
from bot_core.helpers import round_to_next_quarter_hour_timestamp, utc_to_local_timestamp, local_to_utc_timestamp
import base64
import time
import logging

logger = logging.getLogger(__name__)

class MovieNightService:
    def __init__(self, movie_night_manager, movie_manager, movie_scraper: MovieScraper, movie_event_manager, token, guild_id, stream_channel, server_timezone):
        self.guild_id = guild_id
        self.movie_night_manager = movie_night_manager
        self.movie_event_manager = movie_event_manager
        self.movie_manager = movie_manager
        self.movie_scraper = movie_scraper
        self.api_key = movie_scraper.api_key
        self.stream_channel = stream_channel
        self.server_timezone = server_timezone
        self.discord_events = DiscordEvents(token)
        logger.info("MovieNightService initialized")

    async def add_movie_to_movie_night(self, movie_night_id, movie_url):
        logger.debug(f"Attempting to add movie from URL: {movie_url} to movie night ID: {movie_night_id}")
        try:
            self.movie_event_manager.db_session.begin_nested()
            movie_details = self.movie_scraper.get_movie_details_from_url(movie_url)
            logger.debug(f"Received movie details: {movie_details}")

            if not movie_details:
                self.movie_event_manager.db_session.rollback()
                logger.debug("No movie details found, rolling back transaction")
                return None

            existing_movie = self.movie_manager.find_movie_by_name_and_year(movie_details['name'], movie_details['year'])
            if existing_movie:
                movie_id = existing_movie.id
                logger.debug(f"Found existing movie ID: {movie_id}")
            else:
                movie_id = self.movie_manager.save_movie(movie_details)
                logger.debug(f"Saved new movie, ID: {movie_id}")

            movie_night = self.movie_night_manager.find_movie_night_by_id(movie_night_id)
            if not movie_night:
                logger.warning("Movie Night not found")
                return "Movie Night not found"

            last_movie_event = self.movie_event_manager.find_last_movie_event_by_movie_night_id(movie_night_id)
            if last_movie_event and last_movie_event.movie:
                runtime_seconds = last_movie_event.movie.runtime * 60
                last_movie_end_time = last_movie_event.start_time + runtime_seconds
                logger.debug(f"Last movie event end time: {last_movie_end_time}")
            else:
                last_movie_end_time = movie_night.start_time
                logger.debug("No last movie event, using movie night start time")

            new_start_time_unix = max(int(time.time()), last_movie_end_time)
            rounded_time_unix = round_to_next_quarter_hour_timestamp(new_start_time_unix)
            new_start_time_iso = datetime.utcfromtimestamp(rounded_time_unix).isoformat()
            logger.debug(f"Calculated new start time: {new_start_time_iso}")

            new_movie_event_id = self.movie_event_manager.create_movie_event(movie_night_id, movie_id, rounded_time_unix)
            logger.debug(f"Created new movie event ID: {new_movie_event_id}")

            movie_event = self.movie_event_manager.find_movie_event_by_id(new_movie_event_id)
            if movie_event:
                movie = self.movie_manager.find_movie_by_id(movie_event.movie_id)
                if movie:
                    backdrop_url = movie_details.get('backdrop_url', None)
                    if backdrop_url:
                        image_bytes = await download_image(backdrop_url)
                        if image_bytes:
                            converted_image_bytes = convert_image_format(image_bytes, format="JPEG")
                            base64_image = base64.b64encode(converted_image_bytes).decode()
                            image_data = f"data:image/jpeg;base64,{base64_image}"
                        else:
                            image_data = None
                    else:
                        image_data = None
                    if movie.year:
                        event_title = f"{movie.name} ({movie.year})"
                    else:
                        event_title = movie.name
                    discord_event = await self.discord_events.create_event(
                        self.guild_id,
                        self.stream_channel,
                        event_title,
                        movie.overview,
                        new_start_time_iso,
                        image_data=image_data,
                        movie_url=movie_url  
                    )
                    if discord_event and 'id' in discord_event:
                        movie_event.discord_event_id = discord_event['id']
                        self.movie_event_manager.db_session.commit()
                        logger.info(f"Successfully created Discord event: {discord_event['id']}")
                        return (new_movie_event_id, discord_event['id'])
                    else:
                        logger.error(f"Failed to create Discord event: {discord_event}")
                        self.movie_event_manager.db_session.rollback()
                        return None
                else:
                    logger.error("Failed to find movie by ID")
                    self.movie_event_manager.db_session.rollback()
                    return "Failed to create movie event."
            else:
                logger.error("Failed to create movie event in DB")
                self.movie_event_manager.db_session.rollback()
                return "Failed to create movie event."
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            self.movie_event_manager.db_session.rollback()
            return None
    
    async def start_first_event(self, movie_night):
        if movie_night.events:
            first_event = movie_night.events[0]
            await self.discord_events.start_event(self.guild_id, first_event.discord_event_id)
            movie_night.status = 1  # Update status to Started
            movie_night.current_movie_index = 0
            self.movie_event_manager.db_session.commit()

    async def end_last_event(self, movie_night):
        if movie_night.events:
            last_event = movie_night.events[-1]
            await self.discord_events.end_event(self.guild_id, last_event.discord_event_id)
            movie_night.status = 2  # Update status to Finished
            self.movie_event_manager.db_session.commit()

    async def transition_to_next_event(self, movie_night):
        if movie_night.current_movie_index < len(movie_night.events) - 1:
            # End current event
            current_event = movie_night.events[movie_night.current_movie_index]
            await self.discord_events.end_event(self.guild_id, current_event.discord_event_id)

            # Start next event
            movie_night.current_movie_index += 1
            next_event = movie_night.events[movie_night.current_movie_index]
            await self.discord_events.start_event(self.guild_id, next_event.discord_event_id)
            self.movie_event_manager.db_session.commit()