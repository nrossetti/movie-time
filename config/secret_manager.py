import json

class SecretManager:
    def load_secrets(self):
        with open('secrets.json', 'r') as file:
            return json.load(file)