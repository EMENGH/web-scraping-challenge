#!/usr/bin/env python
# coding: utf-8

#dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


# NASA Mars News
# Set Executable Path & Initialize Chrome Browser
#get_ipython().system('which chromedriver')

def init_browser():    
    executable_path = {"executable_path": "/usr/local/bin/chromedriver/"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()

    browser.visit('https://mars.nasa.gov/news/')
    

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    title = soup.find('div', class_='content_title').find('a')

    parag = soup.find('div', class_='article_teaser_body')

    #place results in designated variables to be used later
    news_title = title
    print(f"Title: {news_title}")

    news_p = parag
    print(f"Paragraph: {news_p}")



    # JPL Mars Space Images - Featured Image

    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    

    browser.click_link_by_partial_text('FULL IMAGE')
    
    browser.click_link_by_partial_text('more info')

    feat_html = browser.html
    feat_soup = BeautifulSoup(feat_html,'html.parser')

    mars_img_url = feat_soup.find('figure', class_='lede').a['href']

    orig_url = "https://www.jpl.nasa.gov"
    featured_image_url = orig_url + mars_img_url




    # Mars Facts

    mars_facts_url = 'https://space-facts.com/mars/'

    tables_found = pd.read_html(mars_facts_url)


    mars_facts_df = tables_found[0]
    mars_facts_df.head()


    mars_html_table = mars_facts_df.to_html(classes='data table', index=False, header=False, border=0)
    #mars_html_table = mars_facts_df.to_html()

  

    # Mars Hemispheres

    #browser = Browser('chrome', **executable_path, headless=False)

    #hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    hemis_html = browser.html
    hemis_soup = BeautifulSoup(hemis_html,'html.parser')

    hemis_orig_url = 'https://astrogeology.usgs.gov'

    hemisphere_image_urls = []

    hemis_items = hemis_soup.find_all('div', class_='item')


    # FOR loop to process titles and urls in a dictionary
    for item in hemis_items: 

        title = item.find('h3').text
        partial_img_url = item.find('a', class_='itemLink product-item')['href']

        browser.visit(hemis_orig_url + partial_img_url)
        
        prev_html = browser.html 
        hemis_soup = BeautifulSoup( prev_html, 'html.parser')
    
     
        img_url = hemis_orig_url + hemis_soup.find('img', class_='wide-image')['src']
    
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    # save all the compiled data about mars in a dictionary
    mars_dictionary = {
        "latest_news_title" : news_title,
        "latest_news_parag" : news_p,
        "JPL_featured_image": featured_image_url,
        "mars_facts_table"  : mars_html_table,
        "hemisphere_images" : hemisphere_image_urls
    }   

    # close browser
    browser.quit()

    return mars_dictionary
         





