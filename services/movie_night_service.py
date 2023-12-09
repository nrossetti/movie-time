from services.movie_scraper import MovieScraper
from bot_core.discord_events import DiscordEvents
from datetime import datetime, timedelta
from pytz import utc
from utils.image_util import download_image, convert_image_format
from bot_core.helpers import round_to_next_quarter_hour, utc_to_local, local_to_utc
import base64

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

    async def add_movie_to_movie_night(self, movie_night_id, movie_url):
        try:
            self.movie_event_manager.db_session.begin_nested()
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

            local_last_movie_end_time = utc_to_local(last_movie_end_time, self.server_timezone)
            rounded_local_time = round_to_next_quarter_hour(local_last_movie_end_time)
            new_start_time = local_to_utc(rounded_local_time, self.server_timezone)

            current_time = datetime.now(utc)
            if new_start_time < current_time:
                rounded_current_time = round_to_next_quarter_hour(current_time)
                new_start_time = rounded_current_time

            new_start_time_iso = new_start_time.isoformat()
            new_movie_event_id = self.movie_event_manager.create_movie_event(movie_night_id, movie_id, new_start_time)
            
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
                        image_data=image_data  
                    )
                if discord_event and 'id' in discord_event:
                    movie_event.discord_event_id = discord_event['id']
                    self.movie_event_manager.db_session.commit()
                    return new_movie_event_id
                else:
                    print(f"Failed to create Discord event: {discord_event}")
                    self.movie_event_manager.db_session.rollback()
                    return None
            else:
                self.movie_event_manager.db_session.rollback()
                return "Failed to create movie event."
        except Exception as e:
            print(f"An error occurred: {e}")
            self.movie_event_manager.db_session.rollback()
            return None