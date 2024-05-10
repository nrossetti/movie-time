import discord, re, logging
from datetime import datetime
from bot_core.discord_events import DiscordEvents
from bot_core.discord_actions import create_header_embed, create_movie_embed, post_now_playing, generate_help_pages
from bot_core.helpers import TimeZones, parse_date, parse_start_time, utc_to_local_timestamp, round_to_next_quarter_hour_timestamp
import pytz 

logger = logging.getLogger(__name__)

class MovieCommands:
    def __init__(self, movie_night_manager, movie_night_service, movie_event_manager, discord_token, ping_role_id=None, announcement_channel_id=None):
        self.movie_night_manager = movie_night_manager
        self.movie_night_service = movie_night_service
        self.movie_event_manager = movie_event_manager
        self.announcement_channel_id = announcement_channel_id
        self.ping_role_id  = ping_role_id
        self.discord_events = DiscordEvents(discord_token)
        self.server_timezone = TimeZones.UTC
        logger.info("MovieCommands initialized")

    def parse_movie_urls(self, movie_urls):
        if isinstance(movie_urls, str):
            movie_urls = list(filter(None, re.split(r'[,\t\s]+', movie_urls)))
        elif not isinstance(movie_urls, list):
            movie_urls = []
        logger.info(f"Parsed movie URLs: {movie_urls}")
        return movie_urls

    async def create_movie_night(self, interaction, title: str, description: str, server_timezone_enum: TimeZones, start_time: str = None, start_date: str = None):
        try:
            server_timezone = pytz.timezone(server_timezone_enum.value)
            current_local_datetime = datetime.now(tz=server_timezone)
            parsed_date = parse_date(start_date) if start_date else current_local_datetime.date()

            if parsed_date < current_local_datetime.date():
                await interaction.response.send_message("The specified date must be in the future.")
                return
            if start_date and not start_time:
                await interaction.response.send_message("A start time must be specified for future dates.")
                return
            
            if start_time:
                parsed_time_unix = parse_start_time(start_time, server_timezone_enum, date_str=start_date)
            else:
                parsed_time_unix = int(current_local_datetime.timestamp())

            rounded_time_unix = round_to_next_quarter_hour_timestamp(parsed_time_unix)
            movie_night_id = self.movie_night_manager.create_movie_night(title, description, rounded_time_unix)
            await interaction.response.send_message(f"Movie Night created with ID: {movie_night_id}")
            logger.info(f"Created Movie Night with ID: {movie_night_id}")
        except Exception as e:
            logger.error(f"Error in create_movie_night: {e}")
            raise e

    async def remove_movie_event_command(self, interaction, movie_event_id=None):
        try:
            if movie_event_id is None:
                movie_event_id = self.movie_event_manager.find_last_movie_event()
                
            if movie_event_id is None:
                await interaction.response.send_message("No movie event found to remove.")
                return
            
            discord_event_id, result_message = self.movie_event_manager.remove_movie_event(movie_event_id)
            
            if discord_event_id: 
                await self.discord_events.delete_event(guild_id=interaction.guild.id,event_id=discord_event_id)
            
            await interaction.response.send_message(result_message)
            logger.info(f"Removed movie event: {movie_event_id}")
        except Exception as e:
            logger.error(f"Error in remove_movie_event_command: {e}")
            raise e

    async def add_movies(self, interaction, movie_urls: str or list, movie_night_id: int = None):
        try:
            await interaction.response.defer()
            movie_urls = self.parse_movie_urls(movie_urls)
            if not movie_urls:
                await interaction.followup.send("No valid movie URLs provided.")
                return
            logger.debug(f"Starting to add movies with URLs: {movie_urls} to movie night ID: {movie_night_id}")
            await self.process_movie_urls(interaction, movie_urls, movie_night_id)
            logger.info(f"Added movies to movie night ID {movie_night_id}: {movie_urls}")
        except Exception as e:
            logger.error(f"Error in add_movies: {e}")
            raise e

    async def process_movie_urls(self, interaction, movie_urls: str or list, movie_night_id: int = None):
        try:
            if movie_night_id is None:
                movie_night_id = self.movie_night_manager.get_most_recent_movie_night_id()
                if movie_night_id is None:
                    await interaction.followup.send("No movie nights found.")
                    return

            added_movies = []
            discord_event_ids = []

            for movie_url in movie_urls:
                logger.debug(f"Attempting to add movie from URL: {movie_url} to movie night ID: {movie_night_id}")
                result = await self.movie_night_service.add_movie_to_movie_night(movie_night_id, movie_url)
                logger.debug(f"Received result for movie URL {movie_url}: {result}")
                if not result:
                    logger.debug(f"Failed to add movie: {movie_url}, starting rollback")
                    raise Exception(f'Failed to add movie: "{movie_url}".')


                movie_event_id, discord_event_id = result
                added_movies.append(movie_event_id)
                if discord_event_id:
                    discord_event_ids.append(discord_event_id)

                await interaction.followup.send(f'Added Movie "{movie_url}" to Movie Night. Movie Event ID is: {movie_event_id}')

            logger.info(f"Processed movie URLs for movie night ID {movie_night_id}: {movie_urls}")
        except Exception as e:
            for movie_id in added_movies:
                self.movie_event_manager.remove_movie_event(movie_id)

            for event_id in discord_event_ids:
                await self.discord_events.delete_event(guild_id=interaction.guild.id, event_id=event_id)
            logger.error(f"Exception occurred while processing movies: {e}, rolling back added movies and events")
            await interaction.followup.send(f"An error occurred: {e}. All added movies have been rolled back.")
            logger.error(f"Error in process_movie_urls: {e}")
            raise e

    async def post_movie_night(self, interaction, movie_night_id: int = None):
        await interaction.response.defer()

        if not movie_night_id:
            movie_night_id = self.movie_night_manager.get_most_recent_movie_night_id()
            if not movie_night_id:
                logger.info("No recent Movie Night found.")
                await interaction.followup.send("No recent Movie Night found.")
                return

        try:
            movie_night = self.movie_night_manager.get_movie_night(movie_night_id)
            if not movie_night:
                logger.info(f"No Movie Night found with ID: {movie_night_id}")
                await interaction.followup.send(f"No Movie Night found with ID: {movie_night_id}")
                return

            announcement_channel = interaction.guild.get_channel(self.announcement_channel_id)
            if not announcement_channel:
                logger.info("Announcement channel is not configured.")
                await interaction.followup.send("Announcement channel is not configured.")
                return

            if movie_night.discord_post_id:
                try:
                    existing_post_ids = movie_night.discord_post_id.split(',')
                    for post_id in existing_post_ids:
                        try:
                            await announcement_channel.fetch_message(int(post_id))
                        except discord.NotFound:
                            logger.info(f"Post with ID {post_id} not found. Proceeding with reposting.")
                            raise discord.NotFound

                    message_links = [f"https://discord.com/channels/{interaction.guild.id}/{self.announcement_channel_id}/{post_id}" for post_id in existing_post_ids]
                    await interaction.followup.send(f"Movie Night already posted: {' | '.join(message_links)}")
                    logger.info(f"Movie Night already posted. ID: {movie_night_id}")
                    return
                except discord.NotFound:
                    for post_id in existing_post_ids:
                        try:
                            msg = await announcement_channel.fetch_message(int(post_id))
                            await msg.delete()
                        except discord.NotFound:
                            continue
                    self.movie_night_manager.update_movie_night_post_ids(movie_night_id, "")

            header_embed = create_header_embed(interaction, movie_night, self.ping_role_id)
            movie_embeds = [create_movie_embed(event, index, len(movie_night.events)) for index, event in enumerate(movie_night.events)]
            new_post_ids = []

            for i in range(0, len(movie_embeds), 10):
                embeds_to_post = [header_embed] + movie_embeds[i:i+10] if i == 0 else movie_embeds[i:i+10]
                message = await announcement_channel.send(embeds=embeds_to_post)
                new_post_ids.append(str(message.id))
                logger.info(f"Posted or updated movie night details with message ID {message.id}")

            self.movie_night_manager.update_movie_night_post_ids(movie_night_id, ",".join(new_post_ids))
            await interaction.followup.send(f"Movie Night details posted successfully. ID: {movie_night_id}. Post IDs: {', '.join(new_post_ids)}")
        except Exception as e:
            logger.error(f"An error occurred while posting the Movie Night: {e}")
            await interaction.followup.send("An error occurred while posting the Movie Night.")
    
    async def update_movie_night_post(self, interaction, movie_night_id: int):
        await interaction.response.defer()
        
        movie_night = self.movie_night_manager.get_movie_night(movie_night_id)
        if not movie_night:
            await interaction.followup.send(f"No movie night found with ID: {movie_night_id}")
            return

        announcement_channel = interaction.guild.get_channel(self.announcement_channel_id)
        if not announcement_channel:
            await interaction.followup.send("Announcement channel is not configured correctly.")
            return

        if not movie_night.discord_post_id:
            await interaction.followup.send("This movie night has not been posted yet, so there is nothing to update.")
            return

        existing_post_ids = movie_night.discord_post_id.split(',')
        header_embed = create_header_embed(interaction, movie_night, self.ping_role_id)
        movie_embeds = [create_movie_embed(event, index, len(movie_night.events)) for index, event in enumerate(movie_night.events)]
        all_embeds = [header_embed] + movie_embeds

        embed_chunks = [all_embeds[i:i + 10] for i in range(0, len(all_embeds), 10)]
        new_post_ids = []

        for post_id in existing_post_ids:
            try:
                message = await announcement_channel.fetch_message(int(post_id))
                await message.delete()
            except discord.NotFound:
                pass

        for embed_chunk in embed_chunks:
            message = await announcement_channel.send(embeds=embed_chunk)
            new_post_ids.append(str(message.id))

        self.movie_night_manager.update_movie_night_post_ids(movie_night_id, ",".join(new_post_ids))

        await interaction.followup.send("Movie night details updated successfully.")

    async def view_movie_night(self, interaction, movie_night_id: int = None):
        try:
            await interaction.response.defer()
            if movie_night_id is None:
                movie_night_id = self.movie_night_manager.get_most_recent_movie_night_id()
                if movie_night_id is None:
                    await interaction.followup.send("No movie nights found.")
                    return

            movie_night_details = self.movie_night_manager.get_movie_night_details(movie_night_id)

            if not movie_night_details:
                await interaction.followup.send("Movie Night not found.")
                return

            response_text = f"Movie Night #{movie_night_id}: {movie_night_details['title']}\n"
            response_text += f"Description: {movie_night_details['description']}\n"
            for event in movie_night_details['events']:
                server_timezone_str = self.server_timezone.value
                start_time = utc_to_local_timestamp(event['start_time'], server_timezone_str)
                response_text += f"  - Event ID: {event['event_id']}\n - Name: {event['movie_name']}\n - Start Time: <t:{start_time}:F>\n\n"
            await interaction.followup.send(response_text)
            logger.info(f"Viewed movie night ID {movie_night_id}")
        except Exception as e:
            logger.error(f"Error in view_movie_night: {e}")
            raise e

    async def edit_movie_night(self, interaction, movie_night_id: int = None, title: str = None, description: str = None):
        try:
            if movie_night_id is None:
                movie_night_id = self.movie_night_manager.get_most_recent_movie_night_id()
                if movie_night_id is None:
                    await interaction.followup.send("No movie nights found.")
                    return

            if title or description is not None:
                movie_night_id = self.movie_night_manager.update_movie_night(movie_night_id, title, description)

            await interaction.response.send_message(f"Movie Night updated on ID: {movie_night_id}")
            logger.info(f"Edited movie night ID {movie_night_id}")
        except Exception as e:
            logger.error(f"Error in edit_movie_night: {e}")
            raise e

    async def delete_event(self, interaction, event_id: int):
        try:
            await interaction.response.defer()
            success = self.movie_night_manager.delete_movie_event(event_id)

            if success:
                await interaction.followup.send(f"Successfully deleted Movie Event with ID: {event_id}")
                logger.info(f"Deleted movie event ID {event_id}")
            else:
                await interaction.followup.send("Failed to delete movie event.")
                logger.warning(f"Failed to delete movie event ID {event_id}")
        except Exception as e:
            logger.error(f"Error in delete_event: {e}")
            raise e
    
    async def next_event(self, interaction, movie_night_id: int = None):
        try:
            await interaction.response.defer()
            if not movie_night_id:
                movie_night_id = self.movie_night_manager.get_most_recent_movie_night_id()

            if not movie_night_id:
                await interaction.followup.send("No active Movie Night found.")
                return

            movie_night = self.movie_night_manager.get_movie_night(movie_night_id)
            if not movie_night:
                await interaction.followup.send(f"No Movie Night found with ID: {movie_night_id}")
                return

            if movie_night.status == 0:
                await self.movie_night_service.start_first_event(movie_night)
                current_movie_event = self.movie_night_manager.get_current_movie_event(movie_night_id)
                movie_name = current_movie_event.movie.name if current_movie_event.movie else "Unknown Movie"
                message = f"Started the first movie: {movie_name}"
            elif movie_night.current_movie_index < len(movie_night.events) - 1:
                await self.movie_night_service.transition_to_next_event(movie_night)
                current_movie_event = self.movie_night_manager.get_current_movie_event(movie_night_id)
                movie_name = current_movie_event.movie.name if current_movie_event.movie else "Unknown Movie"
                message = f"Started the next movie: {movie_name}"
            else:
                await self.movie_night_service.end_last_event(movie_night)
                await interaction.followup.send(f"Movie Night has ended.")
                logger.info(f"Ended movie night ID {movie_night_id}.")
                return

            await interaction.followup.send(message)
            now_playing_embed = await post_now_playing(current_movie_event, self.ping_role_id)
            if self.announcement_channel_id:
                announcement_channel = interaction.guild.get_channel(self.announcement_channel_id)
                if announcement_channel and announcement_channel.permissions_for(interaction.guild.me).send_messages:
                    await announcement_channel.send(embed=now_playing_embed)
                else:
                    await interaction.followup.send("Unable to post in the announcement channel.")
                    
        except Exception as e:
            logger.error(f"Error in next_event: {e}")
            await interaction.followup.send("An error occurred while processing the request.")

    async def cancel_movie_night(self, interaction, movie_night_id: int):
        movie_night = self.movie_night_manager.get_movie_night(movie_night_id)
        
        if not movie_night:
            await interaction.response.send_message("Movie Night not found.", ephemeral=True)
            return
        
        for event in movie_night.events:
            if event.discord_event_id:
                await self.discord_events.delete_event(guild_id=interaction.guild.id, event_id=event.discord_event_id)
            self.movie_event_manager.remove_movie_event(event.id)
        
        self.movie_night_manager.delete_movie_night(movie_night_id)
        
        await interaction.response.send_message(f"Movie Night {movie_night_id} and its events have been canceled and deleted.", ephemeral=True)   
                 
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

class HelpCommands:
    def __init__(self):
        logger.info("HelpCommands initialized")

    async def help_command(self, interaction):
        try:
            pages = generate_help_pages()
            view = self.create_view(0, len(pages), pages)
            await interaction.response.send_message(embed=pages[0], view=view, ephemeral=True)
            logger.info("Help command executed")
        except Exception as e:
            logger.error(f"Error in help_command: {e}")
            raise e

    def create_view(self, current_page, total_pages, pages):
        view = discord.ui.View()

        previous_button = discord.ui.Button(label="Previous", style=discord.ButtonStyle.grey, disabled=current_page == 0)
        next_button = discord.ui.Button(label="Next", style=discord.ButtonStyle.grey, disabled=current_page == total_pages - 1)

        async def previous_callback(interaction):
            nonlocal current_page
            current_page -= 1
            new_embed = pages[current_page].set_footer(text=f"Page {current_page + 1} of {total_pages}")
            await interaction.response.edit_message(embed=new_embed, view=self.create_view(current_page, total_pages, pages))
            logger.info(f"Help page {current_page + 1} displayed")

        async def next_callback(interaction):
            nonlocal current_page
            current_page += 1
            new_embed = pages[current_page].set_footer(text=f"Page {current_page + 1} of {total_pages}")
            await interaction.response.edit_message(embed=new_embed, view=self.create_view(current_page, total_pages, pages))
            logger.info(f"Help page {current_page + 1} displayed")

        previous_button.callback = previous_callback
        next_button.callback = next_callback

        view.add_item(previous_button)
        view.add_item(next_button)

        return view