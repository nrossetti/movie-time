import requests
from bs4 import BeautifulSoup
from tmdbv3api import TMDb, Movie, Search

class MovieScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.tmdb = TMDb()
        self.tmdb.api_key = self.api_key
        self.movie = Movie()
    
    def extract_movie_details_from_letterboxd(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title_element = soup.find('h1', class_='headline-1')
            year_element = soup.find('small', class_='number')
            
            if title_element and year_element:
                title = title_element.text.strip()
                year = year_element.text.strip()
                return title, year
            else:
                return None, None
        except Exception as e:
            print(f"An error occurred while extracting details from Letterboxd: {e}")
            return None, None

    def get_movie_details_from_tmdb_by_title_and_year(self, title, year):
        try:
            movie_id = self.search_tmdb_for_movie_id(title, year)
            if movie_id is None:
                return None

            details = self.movie.details(movie_id)
            credits = self.movie.credits(movie_id)
            director = [crew_member for crew_member in credits['crew'] if crew_member['job'] == 'Director']
            
            director_name = director[0]['name'] if director else 'Unknown'
            image_url = f"https://image.tmdb.org/t/p/original{details['poster_path']}"
            backdrop_url = f"https://image.tmdb.org/t/p/original{details['backdrop_path']}"
            runtime = details.get('runtime', 'Unknown')
            budget = details.get('budget', 'Unknown')
            revenue = details.get('revenue', 'Unknown')
            overview = details.get('overview', 'No overview available')
            release_date = details.get('release_date', 'Unknown')

            return {
                'name': details['title'],
                'year': details['release_date'].split('-')[0],
                'director': director_name,
                'image_url': image_url,
                'backdrop_url': backdrop_url,
                'runtime': runtime,
                'budget': budget,
                'revenue': revenue,
                'overview': overview,
                'release_date': release_date,
            }
        except Exception as e:
            print(f"An error occurred while fetching details from TMDB: {e}")
            return None

    def get_movie_details_from_url(self, url):
        if "letterboxd.com" in url:
            title, year = self.extract_movie_details_from_letterboxd(url)
            if title and year:
                return self.get_movie_details_from_tmdb_by_title_and_year(title, year)
        else:
            return None

    def search_tmdb_for_movie_id(self, title, year):
        search = Search()
        results = search.movies({'query': title, 'year': year})
        
        if results:
            return results[0]['id']
        else:
            return None
