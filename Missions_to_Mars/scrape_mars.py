#Import Splinter, BeautifulSoup, Pandas
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {"executable_path": ChromeDriverManager().install()}


def scrape():
    browser = Browser("chrome", **executable_path, headless=False)

    mars_data = {}

# NASA Mars News
# Visitng the Mars NASA News website
url = "https://mars.nasa.gov/news/"
response = requests.get(url)

# Create BeautifulSoup object with html.parser
soup = bs(response.text, 'html.parser')

# Search for news titles
results = soup.find_all('div', class_='content_title')

#Creating a blank list to hold the headlines
news_titles = []

#Creating loop over div elements
for result in results:
    if(result.a):
        if(result.a.text):
            news_titles.append(result)
news_titles

finalnewstitles = []

#Printing the headlines only
for x in range(6):
    var = news_titles[x].text
    newvar = var.strip('\n\n')
    finalnewstitles.append(newvar)

#Find classification for description paragraph below title
presults = soup.find_all('div', class_="rollover_description_inner")

news_p = []
# Loop through the div results to pull out just the text
for x in range(6):
        var=presults[x].text
        newvar = var.strip('\n\n')
        news_p.append(newvar)
    
#add titles and paragraphs to dictionary
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

featured_img_url = a.find("img")["data-src"]
featured_img_url

#Mars facts
# URL to be scraped
url = "https://space-facts.com/mars/"

# Giving defination to the table
table = pd.read_html(url)

# Asking for facts
mars_df = table[0]
mars_df

mars_df.columns = ['Data', 'Measurement']
mars_df.head()

m = pd.Series(mars_df['Data'])
mars_df['Data'] = m.str.strip(':')
mars_df = mars_df.set_index('Data')
mars_df

# Converting into html
html_table = mars_df.to_html()
html_table

#Saving as html file
mars_df.to_html('mars_table.html')

#Mars Hemispheres
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
nextpage_urls = []
imgtitles = []
base_url = 'https://astrogeology.usgs.gov'

#Html object
html = browser.html

#Using Beautiful Soup
soup = bs(html, 'html.parser')

#Getting the info for eleents containing hemisphere photo data
divs = soup.find_all('div', class_='description')

#Iteration to pull titles
counter = 0
for div in divs:
    link = div.find('a')
    href = link['href']
    img_title = div.a.find('h3')
    img_title = img_title.text
    imgtitles.append(img_title)
    next_page = base_url + href
    nextpage_urls.append(next_page)
    counter = counter+1
    if (counter == 4):
        break
print(nextpage_urls)
print(imgtitles)

#Creating loop for high resolution photo on next page
my_images = []
for nextpage_url in nextpage_urls:
    url = nextpage_url
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    link2 = soup.find('img', class_="wide-image")
    forfinal = link2['src']
    full_img = base_url + forfinal
    my_images.append(full_img)
    nextpage_urls = []
my_images

hemispheres_image_urls = []
cerberus = {'title': imgtitles[0], 'img_url': my_images[0]}
schiaparelli = {'title': imgtitles[1], 'img_url': my_images[1]}
syrtis = {'title': imgtitles[2], 'img_url': my_images[2]}
valles = {'title': imgtitles[3], 'img_url': my_images[3]}

hemispheres_image_urls = [cerberus, schiaparelli, syrtis, valles]

print(hemispheres_image_urls)

#adding to dict
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data

if __name__ == "__main__":
    scrape()