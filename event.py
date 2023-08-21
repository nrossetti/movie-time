import requests
import json

def create_discord_event(guild_id, channel_id, name, description, scheduled_start_time, token):
    url = f"https://discord.com/api/v9/guilds/{guild_id}/events"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "channel_id": channel_id,
        "name": name,
        "description": description,
        "scheduled_start_time": scheduled_start_time,
        "privacy_level": 2, # Guild only
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Example usage
guild_id = "443550655265767435"
channel_id = "446417508174397441"
name = "Test Event"
description = "This is a test event."
scheduled_start_time = "2023-08-18T02:30:00Z" # ISO 8601 format
token = "MTEzODkzMDM4NjUyMTU2NzI0Mg.GHCjEP.6N0mAQNJnyKxViO0Dmv-Gj7ALLkimpLqaL3rf4"

event = create_discord_event(guild_id, channel_id, name, description, scheduled_start_time, token)
print(event)