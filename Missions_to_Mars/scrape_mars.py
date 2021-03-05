#Import Splinter, BeautifulSoup, Pandas
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    
def scrape():
    browser = Browser("chrome", **executable_path, headless=False)
    mars_data1 = {}

#NASA Mars News

# Visitng the Mars NASA News website
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)

# Create BeautifulSoup object with html.parser
    soup = bs(response.text, 'html.parser')

 # Search for news titles
    results = soup.find_all('div', class_='content_title')
    results

#Creating a blank list to hold the headlines
news_titles = []
for result in results:
    if (result.a):
        if(result.a.text):
            news_titles.append(result)
            finalnewstitles = []


#Printing the headlines only
for x in range(6):
    var = news_titles[x].text
    newvar = var.strip('\n\n')
    finalnewstitles.append(newvar)

   #add titles and paragraphs to dictionary
    mars_data['news_titles'] = finalnewstitles
    mars_data['news_p'] = news_p


# ## JPL Mars Space Images - Featured Image

# In[10]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


# In[11]:


    #from selenium import webdriver
    'pip install webdriver_manager'


# In[12]:


    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)
    #browser.visit(url)
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')


# In[13]:


#Review html format
    print(soup.prettify())


# In[14]:


    imgs = soup.find_all('a', class_="fancybox")
    imgs


# In[15]:


# pull image link
    feat_img = []
    for img in imgs:
        pic = img['data-fancybox-href']
        feat_img.append(pic)


# In[16]:


    featured_image_url = 'https://www.jpl.nasa.gov' + pic
    featured_image_url
    mars_data['featured_image_url'] = featured_image_url

# ## Mars Facts

# In[17]:


    'pip install lxml'


# In[18]:


    url = 'https://space-facts.com/mars/'


# In[19]:


    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    print(soup.prettify())


# In[20]:


    tables = pd.read_html(url)
    tables[0]


# In[22]:


    mars_df = tables[0]
    mars_df
    mars_df.columns = ['Data', 'Measurement']
    mars_df.head()


# In[25]:


    s = pd.Series(mars_df['Data'])
    mars_df['Data'] = s.str.strip(':')
    mars_df
    mars_df = mars_df.set_index('Data')
    mars_df


# In[26]:


#Use to_html method to generate HTML tables from df
    html_table = mars_df.to_html()
    html_table


# In[27]:


#Save as html file
    mars_df.to_html('mars_table.html')


# ## Mars Hemispheres

# In[34]:


# In[35]:
    

# Setting url for alternate browser
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    nextpage_urls = []
    imgtitles = []
    base_url = 'https://astrogeology.usgs.gov'


# In[36]:


# HTML object
    html = browser.html


# In[37]:


# Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')


# In[38]:


# Retrieve all elements that contain hemisphere photo info
    divs = soup.find_all('div', class_='description')


# In[39]:


# Iterate through each div to pull titles and make list of hrefs to iterate through
    counter = 0
    for div in divs:
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
        link = div.find('a')
        href=link['href']
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


# In[40]:


# Creating loop for high resolution photo on next page

    my_images=[]
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


# In[41]:


# Creating final list of dictionaries
    hemisphere_image_urls = []

    cerberus = {'title':imgtitles[0], 'img_url': my_images[0]}
    schiaparelli = {'title':imgtitles[1], 'img_url': my_images[1]}
    syrtis = {'title':imgtitles[2], 'img_url': my_images[2]}
    valles = {'title':imgtitles[3], 'img_url': my_images[3]}

    hemisphere_image_urls = [cerberus, schiaparelli, syrtis, valles]
    print(hemisphere_image_urls)

#adding to dict
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data

if __name__ == "__main__":
    scrape() 



# #Searching paragraph text under news title
#     p_results = soup.find_all('div', class_='article_teaser_body')

# #Extracting first title and paragraph
#     news_firsttitle = news_titles[0].text
#     news_firstp = p_results[0].text

# #JPL Mars Space Images - Featured Image
# browser = init_browser()





# #Mars Facts

# # URL to be scraped
# url = "https://space-facts.com/mars/"

# # Giving defination to the table
# table = pd.read_html(url)

# # Asking for facts
# mars_facts = table[0]
# mars_facts

# mars_facts.to_html()

# # Mars Hemispheres

# img_url = []
# title = []
# hemisphere_image_urls = []

# url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
# html = requests.get(url).text
# soup = bs(html, 'html.parser')

# results_main_page=soup.find_all("div", class_="item")

# for x in range(len(results_main_page)):
#     image_title = results_main_page[x].a.h3
#     image_title = image_title.get_text()
#     title.append(image_title)

#     link = results_main_page[x].a["href"]
#     main_site = "https://astrogeology.usgs.gov"
#     image_link = main_site + link
#     url = image_link

#     html = requests.get(url).text
#     soup = bs(html, 'html.parser')

#     results=soup.select("ul>li")

#     for x in range(len(results)):
#         if "original" in (results[x].get_text()).lower():
#             each_img_url = results[x].a["href"]
#             img_url.append(each_img_url)
            
#             img_urls_dic={
#                 "title":image_title,
#                 "img_url":each_img_url
#             }
            
#             hemisphere_image_urls.append(img_urls_dic)
            
#             break

# # Store data in a dictionary
#     mars_data = {
#         "latest_news": news_firsttitle,
#         "latest_news_content": news_firstp,
#         "featured_image_url": featured_image_url,
#         "facts_html":mars_facts,
#         "image_urls":hemisphere_image_urls

#     }

# # Return results
#     return scrape
    
# # Close the browser after scraping
# browser.quit()




