from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd 

def scrape():
    # executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # call functions
    news = mars_news(browser)
    fi = mars_featuredimage(browser)
    weather = null

    browser.quit()

    # Return results
    data = {}
    return data

def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    #NASA Mars News
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text

    
    # Store data in a dictionary
    mars = {
        "news_title": news_title,
        "news_p": news_p
    }

    return mars 

def mars_featuredimage(browser):

    return null
