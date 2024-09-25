import pandas as pd
import requests 
from bs4 import BeautifulSoup

url = 'https://leetcode.com/problemset/?page=67'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

print(soup.title.text)