from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Simple Web Scraper is running!"}

@app.get("/scrape")
def scrape_titles():
    url = "https://example.com"  # Replace with a real URL
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch the page"}

    soup = BeautifulSoup(response.text, 'html.parser')
    titles = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]

    return {"titles": titles}
