from datetime import datetime
import discord
from managers.movie_night_manager import MovieNightManager
from bot_core.discord_events import DiscordEvents
from bot_core.discord_actions import create_header_embed, create_movie_embed
from bot_core.helpers import parse_start_time
from bot_core.helpers  import TimeZones, local_to_utc, round_to_next_quarter_hour

class MovieCommands:
    def __init__(self, movie_night_manager, movie_night_service):
        self.movie_night_manager = movie_night_manager
        self.movie_night_service = movie_night_service

    async def create_movie_night(self, interaction, title: str, description: str, server_timezone: TimeZones.UTC, start_time: str = None):
        if server_timezone is None:
            server_timezone = 'UTC'

        if start_time:
            parsed_time = parse_start_time(start_time)
            parsed_time = local_to_utc(parsed_time, server_timezone)
        else:
            parsed_time = datetime.utcnow()
            
        rounded_time = round_to_next_quarter_hour(parsed_time)
        movie_night_id = self.movie_night_manager.create_movie_night(title, description, rounded_time) 
        await interaction.response.send_message(f"Movie Night created with ID: {movie_night_id}")
    
    async def add_movie(self, interaction, movie_url: str, movie_night_id: int = None):
        await interaction.response.defer()

        if movie_night_id is None:
            movie_night_id = self.movie_night_manager.get_most_recent_movie_night_id()
            if movie_night_id is None:
                await interaction.followup.send("No movie nights found.")
                return

        movie_event_id = await self.movie_night_service.add_movie_to_movie_night(movie_night_id, movie_url)

        if movie_event_id:
            await interaction.followup.send(f"Added Movie to Movie Night. Movie Event ID is: {movie_event_id}")
        else:
            await interaction.followup.send("Failed to add movie.")
            return

    async def post_movie_night(self, interaction, movie_night_id: int = None): 
        await interaction.response.defer()
        if not movie_night_id:
            movie_night_id = self.movie_night_manager.get_most_recent_movie_night_id()
            if not movie_night_id:
                await interaction.followup.send("No recent Movie Night found.")
                return

        movie_night = self.movie_night_manager.get_movie_night(movie_night_id)
        if not movie_night:
            await interaction.followup.send(f"No Movie Night found with ID: {movie_night_id}")
            return

        all_embeds = []
        
        header_embed = create_header_embed(interaction, movie_night)
        all_embeds.append(header_embed)

        total_movies = len(movie_night.events)
        for index, movie_event in enumerate(movie_night.events):
            movie_embed = create_movie_embed(movie_event, index, total_movies)
            all_embeds.append(movie_embed)

        await interaction.followup.send(embeds=all_embeds)

class ConfigCommands:
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    async def config(self, interaction, stream_channel: discord.VoiceChannel = None, announcement_channel: discord.TextChannel = None, ping_role: discord.Role = None,  timezone: TimeZones = None):
        response_messages = []
        config_dict = {}

        if not any([stream_channel, announcement_channel, ping_role, timezone]):
            await interaction.response.send_message("Use the config command to set up the movie bot. You can configure the stream channel, announcement channel, and ping role.")
            return
        
        if stream_channel:
            config_dict['stream_channel'] = stream_channel.id
            response_messages.append(f"Stream channel set to {stream_channel.mention}")

        if announcement_channel:
            config_dict['announcement_channel'] = announcement_channel.id
            response_messages.append(f"Announcement channel set to {announcement_channel.mention}")

        if ping_role:
            config_dict['ping_role'] = ping_role.id
            response_messages.append(f"Ping role set to **{ping_role.name}**")

        if timezone:
            config_dict['timezone'] = timezone.value
            response_messages.append(f"Time zone set to **{timezone.name}**")

        self.config_manager.save_settings(interaction.guild.id, config_dict)

        await interaction.response.defer()
        await interaction.followup.send("\n".join(response_messages))

class EventTestCommands:
    def __init__(self, discord_token):
        self.discord_events = DiscordEvents(discord_token)

    async def create_test_event(self, interaction, name: str, description: str, start_time: str, end_time: str):
        guild_id = str(interaction.guild.id)
        event_data = {
            'name': name,
            'description': description,
            'scheduled_start_time': start_time,
            'scheduled_end_time': end_time,
            'entity_type': 3,  
            'privacy_level': 2,
            'entity_metadata': {
                'location': 'Online'
            }
        }
        created_event = await self.discord_events.create_event(guild_id, event_data)
        await interaction.response.send_message(f"Event created: {created_event}")

    async def delete_test_event(self, interaction, event_id: str):
        guild_id = str(interaction.guild.id)
        is_deleted = await self.discord_events.delete_event(guild_id, event_id)
        await interaction.response.send_message(f"Event deleted: {is_deleted}")

    async def modify_test_event(self, interaction, event_id: str, new_name: str):
        guild_id = str(interaction.guild.id)
        updated_data = {'name': new_name}
        modified_event = await self.discord_events.modify_event(guild_id, event_id, updated_data)
        await interaction.response.send_message(f"Event modified: {modified_event}")

    async def list_test_events(self, interaction):
        guild_id = str(interaction.guild.id)
        all_events = await self.discord_events.list_events(guild_id)
        await interaction.response.send_message(f"All events: {all_events}")

    async def start_test_event(self, interaction, event_id: str):
        guild_id = str(interaction.guild.id)
        started_event = await self.discord_events.start_event(guild_id, event_id)
        await interaction.response.send_message(f"Event started: {started_event}")

    async def end_test_event(self, interaction, event_id: str):
        guild_id = str(interaction.guild.id)
        ended_event = await self.discord_events.end_event(guild_id, event_id)
        await interaction.response.send_message(f"Event ended: {ended_event}")