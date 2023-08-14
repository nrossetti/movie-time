from discord import app_commands
from movie_scraper import MovieScraper
from post_generator import create_movie_embed, create_header_embed
from datetime import datetime
import pytz, json, os, re, discord
import json

class MovieBot:
    def __init__(self):
        # Initialization code
        self.latest_post_content = {'embeds': []}
        self.secrets = self.load_secrets()
        self.token = self.secrets['token']
        self.guild_id = self.secrets['guild_id']
        self.api_key = self.secrets['api_key']

        self.intents = discord.Intents.default()
        self.client = discord.Client(intents=self.intents)
        self.tree = app_commands.CommandTree(self.client)

        self.movie_scraper = MovieScraper(self.api_key)

        self.US_TIMEZONE_ABBREVIATIONS = {
            'PST': 'America/Los_Angeles',
            'MST': 'America/Denver',
            'CST': 'America/Chicago',
            'EST': 'America/New_York',
            'AST': 'America/Puerto_Rico',
            'HST': 'America/Adak',
            'AKST': 'America/Anchorage',
        }

        self.define_commands()
        self.client.run(self.token)

    def load_secrets(self):
        with open('secrets.json', 'r') as file:
            return json.load(file)

    def save_setting(self, guild_id, key, value):
        directory = 'settings'
        filename = f'{guild_id}_settings.json'
        filepath = os.path.join(directory, filename)
        
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            with open(filepath, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {}

        settings[key] = value

        try:
            with open(filepath, 'w') as file:
                json.dump(settings, file)
        except Exception as e:
            print(f"An error occurred while saving {filepath}: {str(e)}")

    def get_setting(self, guild_id, setting_name):
        settings_file_path = f"settings/{guild_id}_settings.json" 
        try:
            with open(settings_file_path, 'r') as file:
                settings = json.load(file)
                return settings.get(setting_name)  # Return the value associated with the setting_name, or None if not found
        except FileNotFoundError:
            print(f"Settings file not found for guild ID: {guild_id}")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON in settings file for guild ID: {guild_id}")
            return None
        
    def parse_start_time(self, time_string):
        formats = ['%H:%M', '%I %p', '%I%p', '%I:%M %p', '%I:%M%p'] # Add this format
        for fmt in formats:
            try:
                return datetime.strptime(time_string, fmt).time()
            except ValueError:
                pass

        # Handle the special case of an hour only
        try:
            hour = int(time_string)
            return datetime.strptime(str(hour), '%H').time()
        except ValueError:
            pass

        raise ValueError(f"Time {time_string} is not in expected format")

    async def set_watching(self, movie_name: str):
        activity = discord.Activity(type=discord.ActivityType.watching, name=movie_name)
        await self.client.change_presence(activity=activity)

    def define_commands(self):
        @self.tree.command(name='set_watching', description="Sets the bot's presence to watching a movie.", guild=discord.Object(id=self.guild_id))
        async def set_watching_command(interaction, movie_name: str):
            await self.set_watching(movie_name)  # Call the method using self
            await interaction.response.send_message(f"Set presence to 'Watching {movie_name}'")

        @self.tree.command(name='config', description="Configs the movie bot.", guild=discord.Object(id=self.guild_id))
        async def config(interaction, default_timezone: str = None, stream_channel: discord.VoiceChannel = None, announcement_channel: discord.TextChannel = None, ping_role: discord.Role = None, prefix: str = None):
            response_messages = []

            if not any([default_timezone, stream_channel, announcement_channel, ping_role, prefix]):
                # No arguments provided, so send the default message
                await interaction.response.send_message("Use the config command to set up the movie bot. You can configure the default timezone, stream channel, announcement channel, ping role, and prefix.")
                return
            
            if default_timezone:
                timezone = self.US_TIMEZONE_ABBREVIATIONS.get(default_timezone.upper(), default_timezone)
                if timezone in pytz.all_timezones:
                    self.save_setting(interaction.guild.id, 'default_timezone', timezone)
                    response_messages.append(f"Default timezone set to {default_timezone.upper()} ({timezone})")
                else:
                    response_messages.append(f"Invalid timezone provided!")

            if stream_channel:
                self.save_setting(interaction.guild.id, 'stream_channel', stream_channel.id)
                response_messages.append(f"Stream channel set to {stream_channel.mention}")

            if announcement_channel:
                self.save_setting(interaction.guild.id, 'announcement_channel', announcement_channel.id)
                response_messages.append(f"Announcement channel set to {announcement_channel.mention}")

            if ping_role:
                self.save_setting(interaction.guild.id, 'ping_role', ping_role.id)
                role_name = ping_role.name  # Using the name instead of the mention
                response_messages.append(f"Ping role set to {role_name}")
            
            await interaction.response.defer()
            await interaction.followup.send("\n".join(response_messages))

        @self.tree.command(name='post', description="Posts the most recent generated post.", guild=discord.Object(id=self.guild_id))
        async def post(interaction):
            global latest_post_content

            announcement_channel_id = self.get_setting(interaction.guild.id, 'announcement_channel')
            if announcement_channel_id is None:
                await interaction.response.send_message("Announcement channel ID not found. Make sure it's set correctly.")
                return

            announcement_channel = interaction.guild.get_channel(int(announcement_channel_id))

            if latest_post_content:
                ping_role_id = self.get_setting(interaction.guild.id, 'ping_role')
                
                content_with_ping = ""
                if ping_role_id:
                    ping_role = interaction.guild.get_role(int(ping_role_id))
                    if ping_role:
                        content_with_ping = f"{ping_role.mention}"  # Using role mention to ping

                if announcement_channel:
                    await announcement_channel.send(content_with_ping, embeds=latest_post_content)
                    await interaction.response.send_message("Post sent successfully!")
                else:
                    await interaction.response.send_message("Could not find the announcement channel. Make sure it's set correctly.")
            else:
                await interaction.response.send_message("No recent post found. Please generate a post first.")


        @self.tree.command(name="find_letterboxd_links", description="Finds all Letterboxd links in a specified channel's history.", guild=discord.Object(id=self.guild_id))
        async def find_letterboxd_links(interaction: discord.Interaction, channel: discord.TextChannel):
            pattern = "letterboxd"

            async for message in channel.history(limit=None):
                if pattern in message.content:
                    for word in message.content.split():
                        if pattern in word and word.startswith("http"):
                            await interaction.response.send_message(f"Found link: {word}")

        @self.tree.command(name="create_movie_post", description="Creates a movie post.", guild=discord.Object(id=self.guild_id))
        async def create_post(interaction: discord.Interaction, start_time: str, theme_name: str, description: str, movie_urls: str):
            # Acknowledge the command with a deferred response
            global latest_post_content 

            await interaction.response.defer()

            invoking_user = interaction.user
            invoking_user_name = invoking_user.display_name
            invoking_user_avatar_url = invoking_user.display_avatar

            movie_urls_list = re.split(r'[,\s\t\n]+', movie_urls)
            number_of_movies = len(movie_urls_list)

            start_time_obj_time = self.parse_start_time(start_time)
            start_time_obj = datetime.combine(datetime.today().date(), start_time_obj_time)

            movie_embeds = []

            for index, url in enumerate(movie_urls_list, start=1):
                movie = self.movie_scraper.get_movie_details_from_url(url)

                if movie:
                    movie_embed, next_start_time = create_movie_embed(movie, url, start_time_obj, index, number_of_movies)
                    movie_embeds.append(movie_embed)
                    start_time_obj = next_start_time
                else:
                    await interaction.response.send_message(content=f"Failed to fetch details for movie URL: {url}")
                    return

            header_embed = create_header_embed(number_of_movies, theme_name, description)
            header_embed.set_footer(text=f"Hosted by {invoking_user_name}", icon_url=invoking_user_avatar_url)
            all_embeds = [header_embed] + movie_embeds

            # Send the message after the deferred response
            latest_post_content = all_embeds
            await interaction.followup.send(embeds=all_embeds)

        @self.client.event
        async def on_ready():
            await self.tree.sync(guild=discord.Object(id=self.guild_id))
            print("Ready!")
            await self.set_watching("the previews")  # Call set_watching here

bot = MovieBot()