from datetime import datetime
from managers.movie_night_manager import MovieNightManager
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
    
    async def add_movie(self, interaction, movie_night_id: int, movie_url: str):
        movie_event_id = self.movie_night_service.add_movie_to_movie_night(movie_night_id, movie_url)
        if movie_event_id:
            await interaction.response.send_message(f"Added Movie to Movie Night. Movie Event ID is: {movie_event_id}")
        else:
            await interaction.response.send_message("Failed to add movie.")