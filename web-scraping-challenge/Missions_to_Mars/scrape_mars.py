#import dependencies
import os
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


#initiate browser function

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

#perform scrape

def scrape():

    #initiate browser
    browser = init_browser()

    #scrape news titles

    #URL1
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    #visit the url
    browser.visit(url)

    # Create BS Object
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')

    # Search soup for titles and create a list of the titles
    news_titles=soup.find_all('div', class_='content_title')
    news_title_list=[]
    for title in news_titles:
        news_title_list.append(title.text.strip())
    #print(news_title_list)

    time.sleep(2)

    # Search soup for article teaser text
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    teaser_text_list=[]
    news_teaser_results=soup.find_all('div', class_='article_teaser_body')
    for i in news_teaser_results:
        teaser_text_list.append(i.text.strip())

    #print(teaser_text_list)

    time.sleep(2)

    # Begin new browser session for JPL image search

    url2 = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(url2)
    html2=browser.html
    soup2=BeautifulSoup(html2,'html.parser')
    #soup2

    #Find the first image in the file
    featured_image_url=soup2.find_all("img", class_="BaseImage")[0]["src"]
    #print(featured_image_url)

    #browser.quit()

    time.sleep(2)
    #Collect the Mars Table

    url3='https://space-facts.com/mars/'

    browser.visit(url3)
    html3=browser.html
    soup3=BeautifulSoup(html3,"html.parser")
    soup3_results=soup3.find("table", "tablepress tablepress-id-p-mars")
    soup3_html_content=str(soup3_results)
    #mars_tables_list=pd.read_html("https://space-facts.com/mars/")
    #mars_table_df=mars_tables_list[0]
    #mars_tabel_df1=mars_table_df.rename(columns={0:"Feature",1:"Value"},inplace=False).set_index("Feature")
    #print(mars_tabel_df1)

    #Collect photos of the Martian Hemispheres
    url4='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    html4=browser.html
    #make a soup
    soup4=BeautifulSoup(html4,"html.parser")
    soup4_results=soup4.find_all("div", "description")

    soup4_results=soup4.find_all("div", "description")

    hemi_name_list=[]
    href_list=[]
    furl_list=[]
    image_object_dict={}
    image_object_list=[]
    
    for i in soup4_results:
        hemi_name_list.append(i.a.text)
        #print(hemi_name_list)
        href_list.append(i.a['href'])
        #print(href_list)
        browser.links.find_by_partial_text("Enhanced").click()
        time.sleep(1)
        htmli=browser.html
        #print(html5)
        soupi=BeautifulSoup(htmli,"html.parser")
        soupi_results=soupi.find("a",text="Sample")
        #print(soupi_results)
        furl_list.append(soupi_results['href'])
        #print(furl_list)
        image_object_dict["title"]=i.a.text
        image_object_dict["img_url"]=soupi_results['href']
        image_object_list.append(image_object_dict.copy())
    
    mars_scraped_data={"Headline":news_title_list,"Teaser":teaser_text_list,"JPLFeaturedImage":featured_image_url,"MarsTable":soup3_html_content,"MaritanHemispherePhotos":image_object_list}

    browser.quit()

    return mars_scraped_data


    


