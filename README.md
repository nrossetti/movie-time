<p align="center">
  <img width="128" height="128" src="https://github.com/nrossetti/movie-time/assets/23127108/d73fe97b-31c0-4b66-ab94-4bf5b55bea06" alt="Movie Time Logo">
</p>
<h1 align="center">Movie Time</h1>

&nbsp; &nbsp; &nbsp; &nbsp;Movie Time Bot is a Discord bot designed to facilitate the scheduling and promotion of movie streaming events among friends on Discord. Its purpose is to make watching movies together an enjoyable and easy-to-manage experience. Movie Time's primary functions include configuring settings, generating movie posts, posting the latest movie schedules to specified channels, and managing movie events. Movie Time utilizes Letterboxd for linking movies and extracts detailed information from The Movie Database (TMDb) using their open and free API. Whether it's a casual movie night or a themed marathon, Movie Time brings friends together and takes care of the details. Future developments aim to expand functionality for broader use cases.

---

### Index

- [Features](#features)
  - [Current Functionality](#current-functionality)
  - [Planned Functionality](#planned-functionality)
- [Configuration](#configuration)
  - [Using `secrets.json`](#using-secretsjson)
  - [Using Environment Variables](#using-environment-variables)
- [Commands](#commands)
  - [Configuration Commands](#configuration-commands)
  - [Movie Management Commands](#movie-management-commands)
  - [Utility Commands](#utility-commands)
- [Typical Deployment](#typical-deployment)
- [Dependencies](#dependencies)
- [Notes](#notes)
- [Future Ideas](#future-ideas)
- [Support and Contribution](#support-and-contribution)

---

### Features

#### Current Functionality

1. **Configuration Management**: Administrators can set up the bot's behavior within their guild.
2. **Schedule and Post Generation**: Automatically generates and posts movie schedules.
3. **Event Management**: Allows administrators to create, edit, and delete events.
4. **Multi-Movie Platform Support**: Accepts movie links from Letterboxd and additional sites like IMDb for movie input.

<p align="center">
  <img width=400 height=468 src="https://github.com/nrossetti/movie-time/assets/23127108/3c54397a-f712-4ae6-9cdf-f34163e10fcf">
</p>

#### Planned Functionality

1. **Expanded Event Management**: Automatic creation and management of movie events with richer customization options.
2. **Web Application Component**: A web interface for configuring, editing, and viewing movie nights directly through a browser.

### Configuration

#### `secrets.json` or Environment Variables

Movie Time supports two configuration methods: using a `secrets.json` file or setting environment variables for sensitive information.

##### Using `secrets.json`

The `secrets.json` file stores sensitive information required by the bot, such as API keys and Discord tokens. Ensure this file is properly configured and kept secure.

Example Configuration:
```json
{
    "api_key": "TMDB_api_key",
    "token": "discord_bot_token",
    "guild_id": "guild_id"
}
```

##### Using Environment Variables

Alternatively, you can provide the same information using environment variables:

For Unix/Linux/macOS:
```bash
export TMDB_API_KEY="your_tmdb_api_key"
export DISCORD_BOT_TOKEN="your_discord_bot_token"
export GUILD_ID="your_guild_id"
```

For Windows:
```cmd
set TMDB_API_KEY=your_tmdb_api_key
set DISCORD_BOT_TOKEN=your_discord_bot_token
set GUILD_ID=your_guild_id
```

### Commands

Here are the updated commands available:

#### Configuration Commands

1. **`/config`**
   - Configure the bot's settings for the guild.
   - **Parameters:**
     - `default_timezone`: Set the default timezone for the guild (e.g., 'EST', 'PST').
     - `stream_channel`: Set the VoiceChannel for streaming.
     - `announcement_channel`: Set the TextChannel for announcements.
     - `ping_role`: Set the role to be pinged in announcements.

#### Movie Management Commands

2. **`/post`**
   - Posts the latest generated movie schedule to the configured announcement channel.

3. **`/create_movie_post`**
   - Generates a movie post with details of the movies provided.
   - **Parameters:**
     - `start_time`: The starting time of the event.
     - `theme_name`: The theme name for the movie night.
     - `description`: Description of the event.
     - `movie_urls`: List of movie URLs.

4. **`/delete_event`**
   - Deletes a specified movie event.

5. **`/list_events`**
   - Lists all upcoming movie events in the guild.

#### Utility Commands

6. **`/help`**
   - Displays detailed information about available commands and their usage.

### Typical Deployment

You can deploy Movie Time using Docker for a smooth installation process. Follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/nrossetti/movie-time.git
   cd movie-time
   ```

2. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

3. Set environment variables in a `.env` file or export them directly to the shell:

For Unix/Linux/macOS:
   ```bash
   TMDB_API_KEY="your_tmdb_api_key"
   DISCORD_BOT_TOKEN="your_discord_bot_token"
   GUILD_ID="your_guild_id"
   ```

For Windows:
   ```cmd
   set TMDB_API_KEY=your_tmdb_api_key
   set DISCORD_BOT_TOKEN=your_discord_bot_token
   set GUILD_ID=your_guild_id
   ```

   Alternatively, use a `secrets.json` file as described above.

### Dependencies

- **discord.py**: For Discord API interactions.
- **pytz**: For timezone handling.
- **TMDb API**: For fetching movie details.

### Notes

- Ensure proper permissions are set for the bot to function correctly, including sending messages and accessing roles in the server.
- The bot is designed with security in mind, ensuring sensitive data like tokens and API keys are handled responsibly.

### Future Ideas

- **Letterboxd API Access**: Explore integration with Letterboxd's API to enhance features.
- **Custom Themes and Styles**: Allow for customized movie posts with themes.

### Support and Contribution

For support or to contribute to the development of Movie Time, please contact the repository owner via GitHub.
