class Movie:
    def __init__(self, name, year, director, image_url, backdrop_url, runtime, budget, revenue, overview, release_date, website_links=None):
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
        self.website_links = website_links or {}

    def add_website_link(self, site_name, url):
        self.website_links[site_name] = url

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
        print("Website Links:")
        for site_name, url in self.website_links.items():
            print(f"{site_name}: {url}")