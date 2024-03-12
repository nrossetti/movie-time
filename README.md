<p align="center">
  <img width="128" height="128" src="https://github.com/nrossetti/movie-time/assets/23127108/d73fe97b-31c0-4b66-ab94-4bf5b55bea06" alt="Movie Time Logo">
</p>
<h1 align="center">Movie Time</h1>


&nbsp; &nbsp; &nbsp; &nbsp;Movie Time Bot is a Discord bot designed to facilitate the scheduling and promotion of movie streaming events among friends on Discord. Its purpose is to make watching movies together an enjoyable and easy-to-manage experience. Movie Time primary functions include configuring settings, generating movie posts, posting the latest movie schedules to specified channels, and managing movie events. Movie Time utilizes Letterboxd for linking movies and extracts detailed information from The Movie Database (TMDb) using their open and free API. Whether it's a casual movie night or a themed marathon, Movie Time brings friends together and takes care of the details. While currently tailored to a specific use case, future developments aim to provide more generic implementations and features.

### Features

#### Current Functionality

1. **Configuration Management**: Administrators can set up the bot's behavior within their guild.
2. **Schedule and Post Generation**: Automatically generates and posts movie schedules.

<p align="center">
  <img width=400 height=468 src="https://github.com/nrossetti/movie-time/assets/23127108/3c54397a-f712-4ae6-9cdf-f34163e10fcf">
</p>

#### Planned Functionality

1. **Automatic Event Creation and Management**: Will allow administrators to automatically create and manage movie events, including editing existing events and posts.
2. **Support for Multiple Movie Sites**: In addition to Letterboxd, future updates will allow for movie input links from IMDb and other popular movie platforms.
3. **Docker Compose Deployment**: Support for containerized deployment using Docker Compose, ensuring smooth installation and execution.

### Configuration

#### `secrets.json` Configuration

The `secrets.json` file is used to store sensitive information required by the bot, such as API keys. Ensure this file is properly configured and kept secure.

Example Configuration:
```
{
    "api_key": "TMDB_api_key",
    "token": "discord_bot_token",
    "guild_id": guild_id
}
```
### Commands
**\*\* This outdated - See commands.py or bot.py to see current commands**

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

### Dependencies

- **discord.py** for Discord API interactions.
- **pytz** for timezone handling.

### Notes

- The token used for running the client should be kept private and secure.
- Ensure the proper permissions are set for the bot, particularly for reading and sending messages in channels and accessing role details.
- **Customization**: The current functionality is tailored to a specific use case but will be transitioning to more generic implementation and features as development continues.

### Responsible Data Access

The bot emphasizes responsible data access by leveraging TMDb to obtain detailed movie information and only scrapes the name and date to allow users to use any site to specify a movie. This approach ensures the bot's functionality remains reliable, ethical, and in compliance with various platform terms.

### Future Ideas

- **API Access to Letterboxd**: Exploring the potential integration with Letterboxd's API (if available in the future) would open many new features and enhance the bot's capabilities.

### Support and Contribution

For support or to contribute to the development of Movie Time Bot, please contact the repository owner
