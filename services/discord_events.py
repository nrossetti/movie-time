import aiohttp

class DiscordEvents:
    def __init__(self, discord_token: str):
        self.base_api_url = 'https://discord.com/api/v8'
        self.auth_headers = {
            'Authorization': f'Bot {discord_token}',
            'Content-Type': 'application/json'
        }

    async def create_discord_event(self, guild_id, event_name, event_description, event_start_time, event_end_time):
        event_create_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        event_data = {
            'name': event_name,
            'description': event_description,
            'scheduled_start_time': event_start_time,
            'scheduled_end_time': event_end_time,
            'entity_type': 3
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(event_create_url, headers=self.auth_headers, json=event_data) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    print(f"Failed to create Discord event. Status Code: {response.status}")
                    return None