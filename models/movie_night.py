from datetime import datetime

class MovieNight:
    def __init__(self, theme_name=None, description=None, start_time=None, invoking_user_name=None, invoking_user_avatar_url=None):
        self.theme_name = theme_name
        self.description = description
        self.start_time = start_time or datetime.now()
        self.invoking_user_name = invoking_user_name
        self.invoking_user_avatar_url = invoking_user_avatar_url
        self.movie_events = []

    def add_movie_event(self, movie_event):
        self.movie_events.append(movie_event)

    def set_start_time_for_movie(self, index, time):
        self.movie_events[index].set_start_time(time)