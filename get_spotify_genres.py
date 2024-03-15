import requests
from bs4 import BeautifulSoup


page = requests.get("https://www.chosic.com/list-of-music-genres/")
soup = BeautifulSoup(page.content, 'html.parser')

with open("genres_page.html", "w") as f:
    f.write(soup.prettify())
