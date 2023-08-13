from datetime import timedelta
import discord

class EventManager:
    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def create_event(self, event_details, movie_index):
        movie = event_details['movies'][movie_index]
        start_time = event_details['start_time']
        movie_title = f"{movie['name']} ({movie['year']})"
        event_time = start_time + timedelta(minutes=(movie_index * 15))
        
        event_description = f"Movie screening of {movie_title}\nStart Time: {event_time.strftime('%I:%M %p')}"
        
        guild_id = event_details['guild_id']
        guild = self.bot_client.get_guild(guild_id)
        if guild:
            event_channel_name = "movie-events"  # Replace with your event channel name
            event_channel = discord.utils.get(guild.text_channels, name=event_channel_name)
            
            if event_channel:
                event_message = await event_channel.send(event_description)
                await event_message.pin()  # Pin the event message to keep it visible
                
                return event_message
        
        return None
