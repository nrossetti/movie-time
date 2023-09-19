from datetime import datetime
from managers.movie_night_manager import MovieNightManager
from bot_core.helpers import parse_start_time

class MovieCommands:
    def __init__(self, movie_night_manager):
        self.movie_night_manager = movie_night_manager

    async def create_movie_night(self, interaction, title: str, description: str, start_time: str = None):
        if start_time:
            parsed_time = parse_start_time(start_time)
        else:
            parsed_time = datetime.now()
            
        movie_night_id = self.movie_night_manager.create_movie_night(title, description, parsed_time) 
        await interaction.response.send_message(f"Movie Night created with ID: {movie_night_id}")
