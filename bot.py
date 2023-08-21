from datetime import datetime
import pytz, re, discord
from discord import app_commands
from services.movie_scraper import MovieScraper
from services.discord.event import DiscordEvents
from utils.secret_manager import SecretManager
from utils.config_manager import ConfigManager
from models import MovieEvent, MovieNight
from services import create_movie_embed, create_header_embed
from datetime import timedelta
from math import ceil


class MovieBot:
    def __init__(self):
        # Load secrets and configurations
        self.secret_manager = SecretManager()
        self.secrets = self.secret_manager.load_secrets()
        self.token = self.secrets['token']
        self.guild_id = self.secrets['guild_id']
        self.api_key = self.secrets['api_key']

        self.config_manager = ConfigManager() 

        self.latest_post_content = {'embeds': []}

        self.intents = discord.Intents.default()
        self.client = discord.Client(intents=self.intents)
        self.tree = app_commands.CommandTree(self.client)

        self.movie_scraper = MovieScraper(self.api_key)
        # Initialize DiscordEvents class
        self.discord_events = DiscordEvents(discord_token=self.token)
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

    def parse_start_time(self, time_string):
        formats = ['%H:%M', '%I %p', '%I%p', '%I:%M %p', '%I:%M%p']
        for fmt in formats:
            try:
                return datetime.strptime(time_string, fmt).time()
            except ValueError:
                pass
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
            await self.set_watching(movie_name)
            await interaction.response.send_message(f"Set presence to 'Watching {movie_name}'")

        @self.tree.command(name='config', description="Configs the movie bot.", guild=discord.Object(id=self.guild_id))
        async def config(interaction, default_timezone: str = None, stream_channel: discord.VoiceChannel = None, announcement_channel: discord.TextChannel = None, ping_role: discord.Role = None):
            response_messages = []

            if not any([default_timezone, stream_channel, announcement_channel, ping_role]):
                await interaction.response.send_message("Use the config command to set up the movie bot. You can configure the default timezone, stream channel, announcement channel, ping role, and prefix.")
                return
            
            config_dict = {}
            
            if default_timezone:
                timezone = self.US_TIMEZONE_ABBREVIATIONS.get(default_timezone.upper(), default_timezone)
                if timezone in pytz.all_timezones:
                    config_dict['default_timezone'] = timezone
                    response_messages.append(f"Default timezone set to {default_timezone.upper()} ({timezone})")
                else:
                    response_messages.append(f"Invalid timezone provided!")

            if stream_channel:
                config_dict['stream_channel'] = stream_channel.id
                response_messages.append(f"Stream channel set to {stream_channel.mention}")

            if announcement_channel:
                config_dict['announcement_channel'] = announcement_channel.id
                response_messages.append(f"Announcement channel set to {announcement_channel.mention}")

            if ping_role:
                config_dict['ping_role'] = ping_role.id
                role_name = ping_role.name
                response_messages.append(f"Ping role set to {role_name}")

            self.config_manager.save_settings(interaction.guild.id, config_dict)

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

        @self.tree.command(name="create_movie_post", description="Creates a movie post.", guild=discord.Object(id=self.guild_id))
        async def create_post(interaction: discord.Interaction, start_time: str, theme_name: str, description: str, movie_urls: str):
            global latest_post_content

            await interaction.response.defer()

            invoking_user = interaction.user
            invoking_user_name = invoking_user.display_name
            invoking_user_avatar_url = invoking_user.display_avatar

            movie_urls_list = re.split(r'[,\s\t\n]+', movie_urls)

            # Initial start time
            start_time_obj_time = self.parse_start_time(start_time)
            start_time_obj = datetime.combine(datetime.today().date(), start_time_obj_time)

            # Creating MovieNight object
            movie_night = MovieNight(theme_name, description, invoking_user_name, invoking_user_avatar_url)

            for index, url in enumerate(movie_urls_list, start=1):
                # Getting movie details and creating MovieEvent object
                movie = self.movie_scraper.get_movie_details_from_url(url)

                # Create the movie event with the current start time
                movie_event = MovieEvent(movie, start_time_obj)
                movie_night.add_movie_event(movie_event)  # Adding event to movie_night

                # Assuming movie['runtime'] is the run time in minutes, adjust start_time_obj for the next movie
                run_time_minutes = movie['runtime']
                start_time_obj += timedelta(minutes=run_time_minutes)

                # Round up to the nearest quarter-hour
                minutes = start_time_obj.minute
                next_quarter_hour = (ceil(minutes / 15) * 15) - minutes
                start_time_obj += timedelta(minutes=next_quarter_hour)
                start_time_obj = start_time_obj.replace(second=0, microsecond=0)

            header_embed = create_header_embed(movie_night)
            movie_embeds = [create_movie_embed(event, url, index, len(movie_urls)) for event, url in zip(movie_night.movie_events, movie_urls_list)]


            all_embeds = [header_embed] + movie_embeds
            latest_post_content = all_embeds

            await interaction.followup.send(embeds=all_embeds)
        
        @self.tree.command(name="list_events", description="list_events.", guild=discord.Object(id=self.guild_id))
        async def list(interaction: discord.Interaction):
            response_messages = []
            events = await self.discord_events.list_guild_events(self.guild_id)
            await interaction.followup.send("event list")

        @self.client.event
        async def on_ready():
            await self.tree.sync(guild=discord.Object(id=self.guild_id))
            print("Ready!")
            await self.set_watching("the previews")  # Call set_watching here

bot = MovieBot()