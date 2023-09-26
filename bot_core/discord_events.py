import aiohttp


class DiscordEvents:
    def __init__(self, discord_token):
        self.base_api_url = 'https://discord.com/api/v8'
        self.auth_headers = {
            'Authorization': f'Bot {discord_token}',
            'Content-Type': 'application/json'
        }

    async def create_event(self, guild_id, channel_id, name, description, start_time, image_data=None):
        event_data = {
            'name': name,
            'description': description,
            'scheduled_start_time': start_time,
            'entity_type': 2,
            'channel_id': channel_id,
            'privacy_level': 2,
        }
        print(start_time)
        if image_data:
            event_data['image'] = image_data

        url = f'https://discord.com/api/v8/guilds/{guild_id}/scheduled-events'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.auth_headers, json=event_data) as response:
                return await response.json()

    async def delete_event(self, guild_id, event_id):
        url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events/{event_id}'
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self.auth_headers) as response:
                return response.status == 204

    async def modify_event(self, guild_id, event_id, updated_data):
        url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events/{event_id}'
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, headers=self.auth_headers, json=updated_data) as response:
                return await response.json()

    async def list_events(self, guild_id):
        url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.auth_headers) as response:
                return await response.json()

    async def start_event(self, guild_id, event_id):
        return await self.modify_event(guild_id, event_id, {'status': 2})

    async def end_event(self, guild_id, event_id):
        return await self.modify_event(guild_id, event_id, {'status': 3})
    