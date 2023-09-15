from models.movie import Movie
from models.movie_event import MovieEvent
import aiohttp, json

class DiscordEvents:
    '''Class to create and list Discord events utilizing their API'''
    def __init__(self, discord_token: str) -> None:
        self.base_api_url = 'https://discord.com/api/v8'
        self.auth_headers = {
            'Authorization':f'Bot {discord_token}',
            'User-Agent':'DiscordBot (https://discord.com/api/webhooks/1142979632249970818/5aVo2mZklGdOCA6fw-IsvDCNYmC4g7GafzTFklNLl_BfRESoaRlp0j1vKqLnd4rRAwP9) Python/3.9 aiohttp/3.8.1',
            'Content-Type':'application/json'
        }

    async def list_guild_events(self, guild_id: str) -> list:
        '''Returns a list of upcoming events for the supplied guild ID
        Format of return is a list of one dictionary per event containing information.'''
        event_retrieve_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.get(event_retrieve_url) as response:
                    response.raise_for_status()
                    assert response.status == 200
                    response_list = json.loads(await response.read())
            except Exception as e:
                print(f'EXCEPTION: {e}')
                response_list = [] 

                await session.close()
            return response_list
            
    async def create_guild_event(
        self,
        guild_id: str,
        event_name: str,
        event_description: str,
        event_start_time: str,
        event_end_time: str,
        event_metadata: dict,
        event_privacy_level=2,
        channel_id=None
    ) -> None:
        event_create_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        event_data = json.dumps({
            'name': event_name,
            'privacy_level': event_privacy_level,
            'scheduled_start_time': event_start_time,
            'scheduled_end_time': event_end_time,
            'description': event_description,
            'channel_id': channel_id,
            'entity_metadata': event_metadata,
            'entity_type': 3
        })

        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.post(event_create_url, data=event_data) as response:
                    response_text = await response.text() 
                    response.raise_for_status()
                    assert response.status == 200
            except aiohttp.ClientResponseError as e:
                print(f'EXCEPTION: {e.status}, message=\'{e.message}\', url={e.request_info.url}')
                print(f'Error details: {response_text}')
            except Exception as e:
                print(f'EXCEPTION: {e}')
            finally:
                await session.close()
