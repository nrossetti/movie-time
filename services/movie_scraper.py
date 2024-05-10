import requests
from bs4 import BeautifulSoup
from tmdbv3api import TMDb, Movie, Search
import re
import logging

logger = logging.getLogger(__name__)

class MovieScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.tmdb = TMDb()
        self.tmdb.api_key = self.api_key
        self.movie = Movie()
    
    def normalize_letterboxd_url(self, url: str) -> str:
        logger.debug(f"Normalizing URL: {url}")
        if "boxd.it" in url:
            try:
                response = requests.get(url, allow_redirects=True)
                if response.status_code == 200:
                    logger.debug(f"Resolved URL to: {response.url}")
                    return response.url 
                else:
                    logger.warning(f"Failed to resolve URL: {url}. Status code: {response.status_code}")
                    return None
            except Exception as e:
                logger.error(f"An error occurred while resolving URL: {e}")
                return None
        else:
            return url
        
    def extract_movie_details_from_letterboxd(self, url):
        """ Extracts movie details from a given Letterboxd URL """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title_element = soup.find('h1', class_='headline-1')
            year_element = soup.find('div', class_='releaseyear')

            if title_element and year_element:
                title = title_element.get_text(strip=True).replace(u'\xa0', u' ')
                year = year_element.get_text(strip=True)
                logger.debug(f"Extracted title: {title}, year: {year}")
                return title, year
            else:
                logger.warning("Failed to extract title and/or year.")
                return None, None
        except Exception as e:
            logger.error(f"An error occurred while extracting details from Letterboxd: {e}")
            return None, None


    def get_movie_details_from_tmdb_by_title_and_year(self, title, year):
        logger.debug(f"Fetching movie details from TMDB for title: {title}, year: {year}")
        try:
            movie_id = self.search_tmdb_for_movie_id(title, year)
            if movie_id is None:
                logger.warning(f"No TMDB ID found for movie: {title}, {year}")
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

            logger.debug(f"Extracted TMDB details for {title}")
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
            logger.error(f"An error occurred while fetching details from TMDB: {e}")
            return None

    def get_movie_details_from_url(self, url):
        logger.debug(f"Getting movie details from URL: {url}")
        normalized_url = self.normalize_letterboxd_url(url)
        if normalized_url and "letterboxd.com" in normalized_url:
            title, year = self.extract_movie_details_from_letterboxd(normalized_url)
            if title and year:
                details = self.get_movie_details_from_tmdb_by_title_and_year(title, year)
                if details:
                    details['url'] = normalized_url 
                return details
        else:
            return None

    def search_tmdb_for_movie_id(self, title, year):
        logger.debug(f"Searching TMDB for movie ID with title: {title}, year: {year}")
        search = Search()
        results = search.movies({'query': title, 'year': year})
        
        if results:
            logger.debug(f"Found TMDB ID for {title}: {results[0]['id']}")
            return results[0]['id']
        else:
            logger.warning(f"No results found in TMDB for title: {title}, year: {year}")
            return None
