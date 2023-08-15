class MovieNight:
    def __init__(self, theme_name, description, invoking_user_name, invoking_user_avatar_url):
        self.theme_name = theme_name
        self.description = description
        self.invoking_user_name = invoking_user_name
        self.invoking_user_avatar_url = invoking_user_avatar_url
        self.movie_events = []

    def add_movie_event(self, movie_event):
        self.movie_events.append(movie_event)