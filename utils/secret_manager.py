import json
import os

class SecretManager:
    def load_secrets(self):
        # load secrets from environment variables
        secrets = {
            "api_key": os.getenv("API_KEY"),
            "token": os.getenv("DISCORD_TOKEN"),
            "guild_id": os.getenv("GUILD_ID")
        }

        # If any secret is missing, load value from secrets.json
        missing_secrets = [key for key, value in secrets.items() if value is None]
        if missing_secrets:
            with open('secrets.json', 'r') as file:
                file_secrets = json.load(file)
                for key in missing_secrets:
                    secrets[key] = file_secrets.get(key)

        return secrets