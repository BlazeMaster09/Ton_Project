import requests
from bs4 import BeautifulSoup

link = "https://sploitus.com/search"
responce = requests.get(link).text
soup = BeautifulSoup(responce, 'html.parser')
block = soup.find_all("div")
print(block)