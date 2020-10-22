#!/usr/bin/env python
# coding: utf-8


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


# In[2]:

def init_browser():
#execute chromedriver 
    executable_path = {'executable_path': '/Users/TEMIDAYOAKINSANYA/Documents/JHU_BootCamp/web-scraping-challenge/Missions_to_Mars/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    all_results = {}
#store nasa news url into a variable
    news_url = 'https://mars.nasa.gov/news/'
#vist nasa news url using splinter
    browser.visit(news_url)
    time.sleep(1)
#Extract latest title and paragraph from nasa news website
    soup = BeautifulSoup(browser.html, 'html.parser')
    all_results['news_title'] = soup.find_all('div',class_='content_title')[1].text
    all_results['news_paragraph'] = soup.find_all('div',class_='article_teaser_body')[0].text
#store jpl url into a variable
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#vist jpl url using splinter
    browser.visit(jpl_url)
    time.sleep(1)
    full_image_link=browser.find_by_id("full_image")[0]
    full_image_link.click()
    actual_image_page=browser.links.find_by_partial_text("more info")
    actual_image_page.click()
#Extract latest featured image from nasa jpl website
    soup = BeautifulSoup(browser.html, 'html.parser')
    try:
        jpl_image_url = soup.find('img', class_='main_image')['src']
        all_results['jpl_image_full_url']= str(jpl_url.rsplit('/spaceimages',1)[0])+ str(jpl_image_url)
    except:
        pass

#store twitter url into variable
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
#vist twitter url using splinter
    browser.visit(twitter_url)
    time.sleep(1)
#Extract latest weather tweet from twitter account
    try:
        soup = BeautifulSoup(browser.html, 'html.parser')
        weather_tweet = soup.find('div', attrs={"dir":"auto","lang":"en"}).span.text.rsplit('\n',2)
        all_results['weather_tweet']=str(weather_tweet[0])+str(weather_tweet[1])+str(weather_tweet[2])
    except:
        soup = BeautifulSoup(browser.html, 'html.parser')
        weather_tweet = soup.find('div', attrs={"dir":"auto","lang":"en"}).span.text.rsplit('\n',2)
        all_results['weather_tweet']=str(weather_tweet[0])+str(weather_tweet[1])+str(weather_tweet[2])
#store mars facts url into variable
    mars_facts = 'https://space-facts.com/mars/'
#vist mars facts url using splinter
    browser.visit(mars_facts)
    time.sleep(1)
#Extract table, convert into html, and strip unwanted new lines
    mars_table = pd.read_html(mars_facts)[0]
    mars_table = mars_table.rename(columns= {0:"Properties",1:"Value"})
    mars_table_html = mars_table.to_html()
    mars_table_html = mars_table_html.replace('\n', '')
    all_results['mars_facts'] = mars_table_html
#Mars hemisphere site
    mars_hemisphere='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#Extract cerberus image and image title and store in dictionary
    cerberus = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(cerberus)
    time.sleep(1)
    soup = BeautifulSoup(browser.html, 'html.parser')
    cerberus_image = soup.find("img", class_='wide-image')['src']
    all_results['cer_img_url'] = str(mars_hemisphere.rsplit('/search',1)[0])+ str(cerberus_image)
    all_results['cer_img_title'] = soup.find('h2', class_='title').text
#Extract schiaparelli image and image title and store in dictionary
    schiaparelli = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(schiaparelli)
    time.sleep(1)
    soup = BeautifulSoup(browser.html, 'html.parser')
    schiaparelli_image = soup.find("img", class_='wide-image')['src']
    all_results['sch_img_url'] = str(mars_hemisphere.rsplit('/search',1)[0])+ str(schiaparelli_image)
    all_results['sch_img_title'] = soup.find('h2', class_='title').text
#Extract syrtis_major image and image title and store in dictionary
    syrtis_major = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(syrtis_major)
    time.sleep(1)
    soup = BeautifulSoup(browser.html, 'html.parser')
    syrtis_major_image = soup.find("img", class_='wide-image')['src']
    all_results['sm_img_url'] = str(mars_hemisphere.rsplit('/search',1)[0])+ str(syrtis_major_image)
    all_results['sm_img_title'] = soup.find('h2', class_='title').text
#Extract valles_marineris image and image title and store in dictionary
    valles_marineris = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(valles_marineris)
    time.sleep(1)
    soup = BeautifulSoup(browser.html, 'html.parser')
    valles_marineris_image = soup.find("img", class_='wide-image')['src']
    all_results['vm_img_url'] = str(mars_hemisphere.rsplit('/search',1)[0])+ str(valles_marineris_image)
    all_results['vm_img_title'] = soup.find('h2', class_='title').text
#append dictionary into one list
    #hemisphere_image_urls = []
    #hemisphere_image_urls.extend((cerberus_dict,schiaparelli_dict,syrtis_major_dict,valles_marineris_dict))

    return all_results