class MovieNight:
    def __init__(self, theme, events=[]):
        self.theme = theme
        self.events = events # List of MovieEvent instances

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        self.events.remove(event)