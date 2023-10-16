from discord import Interaction, Embed

def create_header_embed(interaction, movie_night):
    number_map = {1: "SINGLE", 2: "DOUBLE", 3: "TRIPLE", 4: "QUAD", 5: "PENTA", 6: "HEXA"}
    invoking_user = interaction.user
    invoking_user_name = invoking_user.display_name
    invoking_user_avatar_url = invoking_user.display_avatar.url

    number_of_movies = len(movie_night.events)
    announcment = f"{number_map.get(number_of_movies, 'UNKNOWN')} HEADER TONIGHT"
    title = movie_night.title if movie_night.title else 'Unknown Theme'
    description = f"*{movie_night.description if movie_night.description else 'No description available'}*"
    embed = Embed()
    embed.set_author(name=announcment)
    embed.title = title
    embed.description = description
    embed.set_footer(icon_url = invoking_user_avatar_url, text = "hosted by " + invoking_user_name)

    return embed

def create_movie_embed(movie_event, index, total_movies):
    if index == 0:
        position = "Starting off at"
    elif index == total_movies - 1:
        position = "Finishing off at"
    else:
        position = "Then at"

    movie = movie_event.movie
    start_time_string = movie_event.start_time.strftime('%I:%M %p %Z')
    movie_title = f"{movie.name} ({movie.year})"
    director = movie.director.capitalize()
    embed = Embed()
    embed.set_author(name=f"{position} {start_time_string}")
    embed.title = movie_title + "\u200B" * index 
    embed.url = movie.url + "\u200B" * index 

    if movie.image_url:
        embed.set_thumbnail(url=movie.image_url)

    if movie.backdrop_url:
        embed.set_image(url=movie.backdrop_url)

    embed.add_field(name="Director", value=director, inline=True)
    embed.add_field(name="Runtime", value=f"{movie.runtime} minutes", inline=True)
    embed.add_field(name="Release Date", value=movie.release_date, inline=True)

    overview = movie.overview
    if len(overview) > 240:
        last_space_index = overview[:240].rfind(' ')
        overview = overview[:last_space_index] + '...'
    
    embed.description = overview
    return embed
