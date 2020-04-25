import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import re
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'}
    browsers = Browser('chrome', **executable_path, headless=False)
    return browsers
def scrape():
    
    browsers=init_browser()
    url = "https://mars.nasa.gov/news/"

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())

    # results are returned as an iterable list
    titles = soup.find_all('div', class_="content_title")
    #print(titles[0])
    news_titles=titles[0].text.strip()
    print(news_titles)

    # results are returned as an iterable list
    descs = soup.find_all('div', class_="rollover_description_inner")
    #print(descs[0])
    news_p = descs[0].text.strip()
    news_p

    #making executable path
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browsers = Browser('chrome', **executable_path, headless=False)

    #picture url
    pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browsers.visit(pic_url)

    html = browsers.html
    soups = bs(html, 'html.parser')
    #print(soups.prettify())

    feat_pic = soups.find('article',class_='carousel_item')
    anc = feat_pic.find('a')
    image = anc['data-fancybox-href']
    #print(image)

    #cleaning up the URL for the most recent featured image from the webpage.
    mars = '?search=&category=Mars'
    # Use Base URL to Create Absolute URL
    feimg_url = f"https://www.jpl.nasa.gov{image}"
    print(feimg_url)

    #Twitter URL
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    tw_response=requests.get(twitter_url)
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browsers = Browser('chrome', **executable_path, headless=False)
    # launch browser
    #browsers.visit(twitter_url)

        # create beautifulsoup object
    tw_soup = bs(tw_response.text, 'html.parser')

    print(tw_soup)

    #Looking for all paragraph statements in returned object
    mars_weather_tweet = tw_soup.find_all('p', class_ = "")
    mars_weather_tweet

    twite = mars_weather_tweet[0].text.strip()



    results = tw_soup.find_all('div', class_="")
    #tweet = results.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    #tweet_split = tweet.rsplit("pic")
    #mars_weather = tweet_split[0]
    #print(mars_weather)
    print(results)

    #facts table setup
    fact_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(fact_url)
    factual_df = facts_table[0]
    factual_df.columns = ["Category", "Measurement"]
    factual_df = factual_df.set_index("Category")
    factual_df

    tablefacts = factual_df.to_html()

    #image url dictionary
    hem_image_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browsers = Browser('chrome', **executable_path, headless=False)
    browsers.visit(hem_image_url)

    #image information
    imgs_html = browsers.html
    imgs_soup = bs(imgs_html, 'html.parser')
    #print(imgs_soup)

    #looping and getting titles
    site_titles = imgs_soup.find_all("h3")
    for title in site_titles:
        browsers.click_link_by_partial_text("Hemisphere")
            
    print(site_titles)

    picimgs_results = imgs_soup.find_all("div", class_="item")
    picimgs_results

   #looping more to get into dictionary
    imgs_results = imgs_soup.find_all("div", class_="description")
    base_url='https://astrogeology.usgs.gov'
    hemisphere_img_urls=[]
    hrefs=[]
    picture_titles=[]
    for result in picimgs_results:
     # scrape the image title
        images_title = result.find('a', class_='itemLink product-item').text.rstrip("Enhanced")
    # scrape the href link
        rel_image_path = result.a['href']
        hemisphere_image_url = base_url + rel_image_path
     # print article data
    #print(rel_image_path)
    #print(hem_image_url)
    #print(images_title)
        print(hemisphere_image_url)
        hemi_dict = {'title':images_title, 'image_url': hemisphere_image_url}
        hrefs.append(hemisphere_image_url)
        picture_titles.append(images_title)
    #return costa_data

    final_dict = {
        "Latest_Mars_Title": news_titles,
        "News": news_p,
        "Featured_Picture": feimg_url,
        "CerberusHemisphereEnhanced":hrefs[0],
        "SchiaparelliHemisphereEnhanced":hrefs[1],
        "SyrtisMajorHemisphereEnhanced":hrefs[2],
        "VallesMarinerisHemisphereEnhanced":hrefs[3],
        "Twitter": twite,
        "Table": tablefacts}
    print(final_dict)

    return final_dict