class MovieEvent:
    def __init__(self, movie, start_time):
        self.movie = movie  
        self.start_time = start_time 

    def set_start_time(self, time):
        self.start_time = time
