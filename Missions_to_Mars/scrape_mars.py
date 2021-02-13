#Import Splinter, BeautifulSoup, Pandas
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape():

#NASA Mars News

# Visitng the Mars NASA News website
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html

# Create BeautifulSoup object with html.parser
    soup = bs(html, 'html.parser')

# Search for news titles
    news_titles = soup.find_all('div', class_='content_title')

#Searching paragraph text under news title
    p_results = soup.find_all('div', class_='article_teaser_body')

#Extracting first title and paragraph
    news_firsttitle = news_titles[0].text
    news_firstp = p_results[0].text

    print(news_firsttitle)
    print(news_firstp)

#JPL Mars Space Images - Featured Image
browser = init_browser()





#Mars Facts

# URL to be scraped
url = "https://space-facts.com/mars/"

# Giving defination to the table
table = pd.read_html(url)

# Asking for facts
mars_facts = table[0]
mars_facts

mars_facts.to_html()



