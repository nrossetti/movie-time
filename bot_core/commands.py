from datetime import datetime
from managers.movie_night_manager import MovieNightManager
from bot_core.discord_actions import create_header_embed, create_movie_embed
from bot_core.helpers import parse_start_time

class MovieCommands:
    def __init__(self, movie_night_manager, movie_night_service):
        self.movie_night_manager = movie_night_manager
        self.movie_night_service = movie_night_service

    async def create_movie_night(self, interaction, title: str, description: str, start_time: str = None):
        if start_time:
            parsed_time = parse_start_time(start_time)
        else:
            parsed_time = datetime.now()
            
        movie_night_id = self.movie_night_manager.create_movie_night(title, description, parsed_time) 
        await interaction.response.send_message(f"Movie Night created with ID: {movie_night_id}")
    
    async def add_movie(self, interaction, movie_url: str, movie_night_id: int = None):
        if movie_night_id is None:
            movie_night_id = self.movie_night_manager.get_most_recent_movie_night_id()
            if movie_night_id is None:
                await interaction.response.send_message("No movie nights found.")
                return

        movie_event_id = self.movie_night_service.add_movie_to_movie_night(movie_night_id, movie_url)
        if movie_event_id:
            await interaction.response.send_message(f"Added Movie to Movie Night. Movie Event ID is: {movie_event_id}")
        else:
            await interaction.response.send_message("Failed to add movie.")

    async def post_movie_night(self, interaction, movie_night_id: int = None):
        if not movie_night_id:
            movie_night_id = self.movie_night_manager.get_most_recent_movie_night_id()
            if not movie_night_id:
                await interaction.response.send_message("No recent Movie Night found.")
                return

        movie_night = self.movie_night_manager.get_movie_night(movie_night_id)
        if not movie_night:
            await interaction.response.send_message(f"No Movie Night found with ID: {movie_night_id}")
            return

        movie_night = self.movie_night_manager.get_movie_night(movie_night_id)
            
        movie_events_list = [f"Movie Event ID: {movie_event.id}, Movie: {movie_event.movie.name}" for movie_event in movie_night.events]
        await interaction.response.send_message(f"Movie Events: {', '.join(movie_events_list)}")