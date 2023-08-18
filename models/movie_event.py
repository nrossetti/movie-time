from datetime import timedelta

class MovieEvent:
    def __init__(self, movie, start_time):
        self.movie = movie  
        self.start_time = start_time 

    def set_start_time(self, time):
        self.start_time = time

    def round_start_time_to_next_quarter_hour(self):
        minutes_to_next_quarter_hour = 15 - self.start_time.minute % 15
        self.start_time += timedelta(minutes=minutes_to_next_quarter_hour)
