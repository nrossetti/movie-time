import discord
from discord import app_commands
from datetime import datetime
from database.database import SessionLocal
from managers.movie_night_manager import MovieNightManager
from utils.secret_manager import SecretManager
from bot_core.commands import MovieCommands  # Import the class

# Initialize the SecretManager and fetch API key
secrets = SecretManager().load_secrets()
token = secrets['token']
guild_id = secrets['guild_id']

# Initialize DB session and MovieNightManager
db_session = SessionLocal()
movie_night_manager = MovieNightManager(db_session)

# Initialize Bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Initialize MovieCommands class
movie_commands = MovieCommands(movie_night_manager)

@tree.command(name='create_movie_night', description="Create a new movie night", guild=discord.Object(id=guild_id))
async def create_movie_night_command(interaction, title: str, description: str, start_time: str = None):
    try:
        await movie_commands.create_movie_night(interaction, title, description, start_time)  # Use the method from the class
    except ValueError as e:
        await interaction.response.send_message(str(e))

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print("Bot is ready")

client.run(token)