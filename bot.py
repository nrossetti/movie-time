import discord
from discord import app_commands
from database.database import SessionLocal
from utils.secret_manager import SecretManager
from managers.movie_night_manager import MovieNightManager
from managers.movie_manager import MovieManager
from managers.movie_event_manager import MovieEventManager
from services.movie_night_service import MovieNightService
from services.movie_scraper import MovieScraper
from bot_core.commands import MovieCommands, ConfigCommands, HelpCommands
from utils.config_manager import ConfigManager
from bot_core.helpers import TimeZones


config_manager = ConfigManager()
secrets = SecretManager().load_secrets()
token = secrets['token']
guild_id = secrets['guild_id']
api_key = secrets['api_key']
db_session = SessionLocal()
movie_scraper = MovieScraper(api_key)
movie_manager = MovieManager(db_session)
config_manager = ConfigManager()
movie_event_manager = MovieEventManager(db_session)
movie_night_manager = MovieNightManager(db_session)
ping_role = config_manager.get_setting(guild_id, 'ping_role')
announcement_channel = config_manager.get_setting(guild_id, 'announcement_channel')
stream_channel = config_manager.get_setting(guild_id, 'stream_channel')
server_timezone_str = config_manager.get_setting(guild_id, 'timezone') or 'UTC'
server_timezone = next((tz for tz in TimeZones if tz.value == server_timezone_str), None)
movie_night_service = MovieNightService(movie_night_manager, MovieManager(db_session), movie_scraper, movie_event_manager, token, guild_id, stream_channel, server_timezone)
movie_commands = MovieCommands(movie_night_manager, movie_night_service, movie_event_manager, token, ping_role, announcement_channel)
config_commands = ConfigCommands(config_manager)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



@tree.command(name='create_movie_night', description="Create a new movie night", guild=discord.Object(id=guild_id))
async def create_movie_night_command(interaction, title: str, description: str, start_time: str = None, start_date: str = None):
    try:
        await movie_commands.create_movie_night(interaction, title, description, server_timezone, start_time, start_date )
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='add_movies', description="Add movies to a movie night", guild=discord.Object(id=guild_id))
async def add_movies_command(interaction,  movie_urls: str or list, movie_night_id: int = None):
    try:
        await movie_commands.add_movies(interaction, movie_urls, movie_night_id)
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='remove_movie_event', description="Remove a movie event from a movie night", guild=discord.Object(id=guild_id))
async def remove_movie_event_command(interaction, movie_event_id: int = None):
    try:
        await movie_commands.remove_movie_event_command(interaction, movie_event_id)
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='post_movie_night', description="Post the movie night", guild=discord.Object(id=guild_id))
async def post_movie_night_command(interaction, movie_night_id: int = None):
    try:
        await movie_commands.post_movie_night(interaction, movie_night_id)
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='view_movie_night', description="View details of a movie night", guild=discord.Object(id=guild_id))
async def view_movie_night_command(interaction, movie_night_id: int = None):
    try:
        await movie_commands.view_movie_night(interaction, movie_night_id)
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='edit_movie_night', description="Edit a movie night", guild=discord.Object(id=guild_id))
async def edit_movie_night_command(interaction, movie_night_id: int = None, title: str = None, description: str = None):
    try:
        await movie_commands.edit_movie_night(interaction, movie_night_id, title, description )
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='delete_event', description="Delete a movie event", guild=discord.Object(id=guild_id))
async def delete_event_command(interaction, event_id: int):
    try:
        await movie_commands.remove_movie_event_command(interaction, event_id)
    except ValueError as e:
        await interaction.response.send_message(str(e))
        
@tree.command(name='config', description="Configs the movie bot.", guild=discord.Object(id=guild_id))
async def config_command(interaction, stream_channel: discord.VoiceChannel = None, announcement_channel: discord.TextChannel = None, ping_role: discord.Role = None, timezone: TimeZones = None):
    await config_commands.config(interaction, stream_channel, announcement_channel, ping_role, timezone)

@tree.command(name='next', description="Start the next movie", guild=discord.Object(id=guild_id))
async def next_event_command(interaction, movie_night_id: int = None):
    try:
        await movie_commands.next_event(interaction, movie_night_id)
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='help', description="Displays help information for bot commands", guild=discord.Object(id=guild_id))
async def help_command(interaction):
    help_commands = HelpCommands()
    await help_commands.help_command(interaction)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print("Bot is ready")

client.run(token)