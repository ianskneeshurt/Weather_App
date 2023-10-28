import requests
from bs4 import BeautifulSoup

url = "https://www.weather.gov/slc/flashflood"
webpage = requests.get(url)

soup = BeautifulSoup(webpage.content, "html.parser")
flood_table = soup.find('table', id="RRA_TABLE")

print(flood_table)