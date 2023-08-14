from datetime import datetime, timedelta, timezone
import math, re
from discord import Embed

def create_header_embed(number_of_movies, theme_name, description):
    number_map = {1: "SINGLE", 2: "DOUBLE", 3: "TRIPLE", 4: "QUAD", 5: "PENTA", 6: "HEXA"}

    author_name = f"{number_map.get(number_of_movies, 'UNKNOWN')} HEADER TONIGHT"
    title = theme_name if theme_name else 'Unknown Theme'
    description = f"*{description if description else 'No description available'}*"
    embed = Embed()
    embed.set_author(name=author_name)
    embed.title = title
    embed.description = description
    
    return embed

def create_movie_embed(movie, movie_url, start_time_obj, movie_index, number_of_movies):
    positions = ["Starting off at", "Then at", "Finishing off at"]
    position = positions[0] if movie_index == 1 else (positions[1] if movie_index < number_of_movies else positions[2])

    movie_title = f"{movie.get('name', 'Unknown Movie')} ({movie.get('year', 'Unknown Year')})"

    if movie_index > 1:  # Update only if it's not the first movie
        runtime_minutes = int(movie.get('runtime', 0))
        rounded_runtime = int(math.ceil(runtime_minutes / 15.0)) * 15
        next_start_time = start_time_obj + timedelta(minutes=rounded_runtime)
    else:
        next_start_time = start_time_obj

    start_time_string = next_start_time.strftime('%I:%M %p %Z')


    director = movie.get('director', 'Unknown Director').capitalize()
    movie_details = f"**{position}** {movie_title} at {start_time_string}\nDirected by {movie.get('director', 'Unknown Director')}"


    embed = Embed()
    embed.set_author(name=f"{position} {start_time_string}")
    embed.title = movie_title
    embed.url = movie_url

    if 'image_url' in movie and movie['image_url']:
        image_url = movie['image_url']
        embed.set_thumbnail(url=image_url)

    if 'backdrop_url' in movie and movie['backdrop_url']:
        backdrop_url = movie['backdrop_url']
        embed.set_image(url=backdrop_url)

    # Add fields for additional movie information
    embed.add_field(name="Director", value= director, inline=True)
    embed.add_field(name="Runtime", value=f"{movie.get('runtime', 'Unknown')} minutes", inline=True)
    embed.add_field(name="Release Date", value=movie.get('release_date', 'Unknown'), inline=True)
    
    def shorten_number(number):
        if number >= 1000000:
            return f"{number / 1000000:.1f} mil"
        elif number >= 1000:
            return f"{number / 1000:.0f} k"
        else:
            return str(number)

    budget, revenue = movie.get('budget', 0), movie.get('revenue', 0)
    embed.add_field(name="Budget | Revenue", value=f"{'-' if budget==0 else shorten_number(budget)} | {'-' if revenue==0 else shorten_number(revenue)}", inline=True)

    overview = movie.get('overview', 'No overview available')
    if len(overview) > 240:
        last_space_index = overview[:240].rfind(' ')
        overview = overview[:last_space_index] + '...'
    
    embed.description = movie_details + "\n" + overview
    return embed, next_start_time

