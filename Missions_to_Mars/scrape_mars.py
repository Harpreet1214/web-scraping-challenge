#Import Splinter, BeautifulSoup, Pandas
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    #browser = Browser("chrome", **executable_path, headless=False)

    mars_data = {}

#Set the executable path and initialize the chrome browser in splinter
executable_path = {"executable_path": ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path, headless=False)

# NASA Mars News
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

#adding titles and paragraph to dictionary
mars_data['news_titles'] = finalnewstitles
mars_data['news_p'] = news_p

#Featured Image
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
#html = browser.html

browser.find_by_xpath("/html/body/div/div/div/header/div[1]/div[3]/div/nav/div[1]/div[4]/button/span").click()

browser.find_by_xpath("/html/body/div/div/div/header/div[1]/div[3]/div/nav/div[1]/div[4]/div/div/div/div/div[1]/div/div/div/a/div/div/div/div/img").click()

#browser.find_by_xpath("/html/body/div/div/div/main/div/div[2]/div/div/div[1]/img").click()

img_browser = browser.html
soup_img = bs(img_browser, "html.parser")

a = soup_img.find("div", class_="BaseImagePlaceholder")

a.find("img")["data-src"]

#Mars facts
# URL to be scraped
url = "https://space-facts.com/mars/"

# Giving defination to the table
table = pd.read_html(url)

# Asking for facts
mars_facts = table[0]
mars_facts

mars_facts.to_html()

#Mars Hemispheres
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

hemisphere_image_urls

#adding to dict
mars_data["hemisphere_image_urls"] = hemisphere_image_urls

return mars_data

if __name__ == "__main__":
    scrape()
