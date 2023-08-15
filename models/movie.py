class Movie:
    def __init__(self, name, year, director, image_url, backdrop_url, runtime, budget, revenue, overview, release_date):
        self.name = name
        self.year = year
        self.director = director
        self.image_url = image_url
        self.backdrop_url = backdrop_url
        self.runtime = runtime
        self.budget = budget
        self.revenue = revenue
        self.overview = overview
        self.release_date = release_date

    def display_details(self):
        print(f"Title: {self.name}")
        print(f"Year: {self.year}")
        print(f"Director: {self.director}")
        print(f"Runtime: {self.runtime} minutes")
        print(f"Budget: ${self.budget}")
        print(f"Revenue: ${self.revenue}")
        print(f"Overview: {self.overview}")
        print(f"Release Date: {self.release_date}")
        print(f"Image URL: {self.image_url}")
        print(f"Backdrop URL: {self.backdrop_url}")