## Movie Time Bot

### Description
## Movie Time Bot

### Description

Movie Time Bot is a Discord bot designed to facilitate the scheduling and promotion of movie streaming events among friends on Discord. Its purpose is to make watching movies together an enjoyable and easy-to-manage experience. The bot's primary functions include configuring settings, generating movie posts, posting the latest movie schedules to specified channels, and managing movie events. Whether it's a casual movie night or a themed marathon, Movie Time Bot brings friends together and takes care of the details. While currently tailored to a specific use case, future developments aim to provide more generic implementations and features.

### Features

#### Current Functionality

1. **Configuration Management**: Administrators can set up the bot's behavior within their guild.
2. **Schedule and Post Generation**: Automatically generates and posts movie schedules.

#### Planned Functionality

1. **Automatic Event Creation and Management**: Will allow administrators to automatically create and manage movie events, including editing existing events and posts.
2. **Docker Compose Deployment**: Support for containerized deployment using Docker Compose, ensuring smooth installation and execution.

### Configuration

#### `secrets.json` Configuration

The `secrets.json` file is used to store sensitive information required by the bot, such as API keys. Ensure this file is properly configured and kept secure.

Example Configuration:
```
{
  "api_key": "your_api_key_here",
  "discord_token": "your_discord_token_here"
}
```
### Commands

#### 1. `/config`

This command is used to configure the bot's settings.

- **Parameters:**
  - `default_timezone`: Set the default timezone for the guild (e.g., 'EST', 'PST').
  - `stream_channel`: Set the VoiceChannel where the streaming will occur.
  - `announcement_channel`: Set the TextChannel where announcements will be made.
  - `ping_role`: Set the role that will be pinged in announcements.

#### 2. `/post`

This command posts the most recent generated movie schedule to the configured announcement channel.

#### 3. `/create_movie_post`

This command generates a movie post including details of the movies provided.

- **Parameters:**
  - `start_time`: The starting time of the event.
  - `theme_name`: Theme name for the movie night.
  - `description`: Description of the movie event.
  - `movie_urls`: A list of URLs to the movies.

### Configuration Files

Settings for each guild are stored in JSON files located in the `/settings` directory, following the format `guildid_settings.json`.

### Events

- `on_ready`: Called when the bot is ready and
- 
### Dependencies

- **discord.py** for Discord API interactions.
- **pytz** for timezone handling.

### Notes

- The token used for running the client should be kept private and secure.
- Ensure the proper permissions are set for the bot, particularly for reading and sending messages in channels and accessing role details.
- **Customization**: The current functionality is tailored to a specific use case but will be transitioning to more generic implementation and features as development continues.

### Support and Contribution

For support or to contribute to the development of Movie Time Bot, please contact the repository owner or follow the guidelines provided in the repository's contributing documentation.

### Project Management

Track the development progress and participate in planning on our [Trello board](https://trello.com/b/aQVszL6b/movie-bot).
 successfully connected to Discord.
