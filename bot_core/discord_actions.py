from discord import Embed
from datetime import datetime

def create_header_embed(interaction, movie_night, ping_role_id):
    number_map = {1: "SINGLE", 2: "DOUBLE", 3: "TRIPLE", 4: "QUAD", 5: "PENTA", 6: "HEXA"}
    invoking_user = interaction.user
    invoking_user_name = invoking_user.display_name
    invoking_user_avatar_url = invoking_user.display_avatar.url
    number_of_movies = len(movie_night.events)
    announcment = f"{number_map.get(number_of_movies, 'UNKNOWN')} HEADER TONIGHT"
    title = movie_night.title
    description = f"*{movie_night.description if movie_night.description else 'No description available'}*"
    if ping_role_id:
        ping_role_mention = f"<@&{ping_role_id}>"
        description += f"\n\n{ping_role_mention}"
    embed = Embed()
    embed.set_author(name=announcment)
    embed.title = title
    embed.add_field(name=f"<t:{movie_night.start_time}:F>", value=description, inline=False)
    embed.set_footer(icon_url = invoking_user_avatar_url, text = "hosted by " + invoking_user_name)

    return embed

def create_movie_embed(movie_event, index, total_movies):
    if index == 0:
        position = "Starting off with"
    elif index == total_movies - 1:
        position = "Finishing off with"
    else:
        position = "Followed by"

    movie = movie_event.movie
    start_time_string = f"<t:{movie_event.start_time}:t>"
    movie_title = f"{movie.name} ({movie.year})"
    director = movie.director.capitalize()
    embed = Embed()
    embed.set_author(name=f"{position}")
    embed.title = movie_title 
    embed.url = movie.url + f"?{index}"
    if movie.image_url:
        embed.set_thumbnail(url=movie.image_url)

    if movie.backdrop_url:
        embed.set_image(url=movie.backdrop_url)

    start_time = "at " + start_time_string
    overview = movie.overview
    if len(overview) > 240:
        last_space_index = overview[:240].rfind(' ')
        overview = overview[:last_space_index] + '...'
    
    embed.description = start_time
    embed.add_field(name="Overview", value=overview, inline=False)
    embed.add_field(name="Director", value=director, inline=True)
    embed.add_field(name="Runtime", value=f"{movie.runtime} minutes", inline=True)
    embed.add_field(name="Release Date", value=movie.release_date, inline=True)

    return embed

async def post_now_playing(movie_event, ping_role_id):
    movie = movie_event.movie
    movie_title = f"{movie.name} ({movie.year})"
    ping_role_mention = f"<@&{ping_role_id}>" if ping_role_id else ""

    embed = Embed()
    embed.title = movie_title
    embed.url = movie.url
    embed.description = f"{ping_role_mention}"

    if movie.image_url:
        embed.set_image(url=movie.image_url)

    return embed