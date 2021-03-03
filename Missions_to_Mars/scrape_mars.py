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

# Mars Hemispheres

img_url = []
title = []
hemisphere_image_urls = []

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
html = requests.get(url).text
soup = bs(html, 'html.parser')

results_main_page=soup.find_all("div", class_="item")

for x in range(len(results_main_page)):
    image_title = results_main_page[x].a.h3
    image_title = image_title.get_text()
    title.append(image_title)

    link = results_main_page[x].a["href"]
    main_site = "https://astrogeology.usgs.gov"
    image_link = main_site + link
    url = image_link

    html = requests.get(url).text
    soup = bs(html, 'html.parser')

    results=soup.select("ul>li")

    for x in range(len(results)):
        if "original" in (results[x].get_text()).lower():
            each_img_url = results[x].a["href"]
            img_url.append(each_img_url)
            
            img_urls_dic={
                "title":image_title,
                "img_url":each_img_url
            }
            
            hemisphere_image_urls.append(img_urls_dic)
            
            break

# Store data in a dictionary
    mars_data = {
        "latest_news": news_firsttitle,
        "latest_news_content": news_firstp,
        "featured_image_url": featured_image_url,
        "facts_html":mars_facts,
        "image_urls":hemisphere_image_urls

    }

# Return results
    return scrape
    
# Close the browser after scraping
browser.quit()




