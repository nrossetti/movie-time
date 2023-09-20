import discord
from discord import app_commands
from datetime import datetime
from database.database import SessionLocal
from utils.secret_manager import SecretManager
from managers.movie_night_manager import MovieNightManager
from managers.movie_manager import MovieManager
from managers.movie_event_manager import MovieEventManager
from services.movie_night_service import MovieNightService
from services.movie_scraper import MovieScraper
from bot_core.commands import MovieCommands, ConfigCommands # Import the class
from utils.config_manager import ConfigManager


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
movie_night_service = MovieNightService(movie_night_manager, MovieManager(db_session), movie_scraper, movie_event_manager)
movie_commands = MovieCommands(movie_night_manager, movie_night_service)
config_commands = ConfigCommands(config_manager)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name='create_movie_night', description="Create a new movie night", guild=discord.Object(id=guild_id))
async def create_movie_night_command(interaction, title: str, description: str, start_time: str = None):
    try:
        await movie_commands.create_movie_night(interaction, title, description, start_time)  # Use the method from the class
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='add_movie', description="Add a movie to a movie night", guild=discord.Object(id=guild_id))
async def add_movie_command(interaction,  movie_url: str, movie_night_id: int = None):
    try:
        await movie_commands.add_movie(interaction, movie_url, movie_night_id)
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='post_movie_night', description="Post the movie night", guild=discord.Object(id=guild_id))
async def post_movie_night_command(interaction, movie_night_id: int = None):
    try:
        await movie_commands.post_movie_night(interaction, movie_night_id)
    except ValueError as e:
        await interaction.response.send_message(str(e))

@tree.command(name='config', description="Configs the movie bot.", guild=discord.Object(id=guild_id))
async def config_command(interaction, stream_channel: discord.VoiceChannel = None, announcement_channel: discord.TextChannel = None, ping_role: discord.Role = None):
    await config_commands.config(interaction, stream_channel, announcement_channel, ping_role)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print("Bot is ready")

client.run(token)