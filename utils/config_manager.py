import os
import json

class ConfigManager:
    def __init__(self):
        self.directory = 'storage/settings'

    def save_settings(self, guild_id, settings_dict):
        filename = f'{guild_id}_settings.json'
        filepath = os.path.join(self.directory, filename)
        
        # Create the directory if it doesn't exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        try:
            with open(filepath, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {}

        settings.update(settings_dict)

        try:
            with open(filepath, 'w') as file:
                json.dump(settings, file)
        except Exception as e:
            print(f"An error occurred while saving {filepath}: {str(e)}")

    def get_setting(self, guild_id, setting_name):
        settings_file_path = os.path.join(self.directory, f"{guild_id}_settings.json") 
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

    def get_all_settings(self, guild_id):
        settings_file_path = os.path.join(self.directory, f"{guild_id}_settings.json")
        try:
            with open(settings_file_path, 'r') as file:
                settings = json.load(file)
                return settings  # Return all settings
        except FileNotFoundError:
            print(f"Settings file not found for guild ID: {guild_id}")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON in settings file for guild ID: {guild_id}")
            return None