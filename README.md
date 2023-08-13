## Movie Time Bot

### Description

Movie Time Bot is a Discord bot designed to facilitate the scheduling and promotion of movie streaming events. The bot allows administrators to configure settings, generate movie posts, and post the latest movie schedule to a specified channel.

### Commands

#### 1. `/config`

This command is used to configure the bot's settings.

- **Parameters:**
  - `default_timezone`: Set the default timezone for the guild (e.g., 'EST', 'PST').
  - `stream_channel`: Set the VoiceChannel where the streaming will occur.
  - `announcement_channel`: Set the TextChannel where announcements will be made.
  - `ping_role`: Set the role that will be pinged in announcements.
  - `prefix`: Set a prefix for the bot's commands (not used in the provided code).

#### 2. `/post`

This command posts the most recent generated movie schedule to the configured announcement channel.

#### 3. `/find_letterboxd_links`

This command searches for all Letterboxd links in a specified channel's history.

- **Parameters:**
  - `channel`: Specify the TextChannel to search for links.

#### 4. `/create_movie_post`

This command generates a movie post including details of the movies provided.

- **Parameters:**
  - `start_time`: The starting time of the event.
  - `theme_name`: Theme name for the movie night.
  - `description`: Description of the movie event.
  - `movie_urls`: A list of URLs to the movies.

### Configuration Files

Settings for each guild are stored in JSON files located in the `/settings` directory, following the format `guildid_settings.json`.

### Events

- `on_ready`: Called when the bot is ready and successfully connected to Discord.

### Dependencies

- **discord.py** for Discord API interactions.
- **pytz** for timezone handling.
- **movie_scraper.py** for movie details scraping.
- **post_generator.py** for generating post embeds.

### Notes

- The token used for running the client should be kept private and secure.
- Ensure the proper permissions are set for the bot, particularly for reading and sending messages in channels and accessing role details.

### Support and Contribution

For support or to contribute to the development of Movie Time Bot, please contact the repository owner or follow the guidelines provided in the repository's contributing documentation.
