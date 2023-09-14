from database.db_models import Movie
from database.database import SessionLocal, engine, Base
from managers.movie_manager import MovieManager
from services.movie_scraper import MovieScraper
from utils.secret_manager import SecretManager

# Initialize database
Base.metadata.create_all(bind=engine)

# Initialize Secret Manager and load API key
secret_manager = SecretManager()
secrets = secret_manager.load_secrets()
api_key = secrets["api_key"]

# Initialize MovieScraper
movie_scraper = MovieScraper(api_key)

# Scrape a movie (replace with an actual URL)
url = "https://letterboxd.com/film/national-treasure/"  # Replace with a real Letterboxd URL
movie_details = movie_scraper.get_movie_details_from_url(url)

# Create a new database session
db_session = SessionLocal()

# Initialize MovieManager
movie_manager = MovieManager(db_session)

# Save the movie to the database
movie_id = movie_manager.save_movie(movie_details)

# Query the database to ensure the movie was saved correctly
saved_movie = db_session.query(Movie).filter_by(id=movie_id).first()

print(f"Saved movie: {saved_movie.name}")

# Close the database session
db_session.close()
