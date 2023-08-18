class MovieNight:
    def __init__(self, theme_name=None, description=None, invoking_user_name=None, invoking_user_avatar_url=None):
        self.theme_name = theme_name
        self.description = description
        self.invoking_user_name = invoking_user_name
        self.invoking_user_avatar_url = invoking_user_avatar_url
        self.movie_events = []

    def add_movie_event(self, movie_event):
        self.movie_events.append(movie_event)

    def set_start_time_for_movie(self, index, time):
        self.movie_events[index].set_start_time(time)

    def calculate_start_times(self):
        # Automatic calculation of start times based on movie runtimes
        pass

class MovieNightManager:
    def __init__(self, theme_name=None, description=None, invoking_user_name=None, invoking_user_avatar_url=None):
        self.movie_nights = []

    def create_movie_night(self, theme_name, description):
        movie_night = MovieNight(theme_name, description)
        self.movie_nights.append(movie_night)
        return movie_night

    def get_movie_night(self, index):
        return self.movie_nights[index]