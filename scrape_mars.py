from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd 

def scrape():
    # executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # call functions
    news = mars_news(browser)
    fi = mars_featuredimage(browser)
    mtw = mars_weather(browser)
    table = mars_table(browser)

    browser.quit()

    # Return results
    data = {"news": news,
    "fi": fi,
    "mtw": mtw,
    "table": table}   

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
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    href = soup.find('a', class_="button fancybox").get('data-fancybox-href')
    featured_image_url = (f"https://www.jpl.nasa.gov{href}")

    jpl = {"featured_image_url": featured_image_url}

    return jpl

def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    p_mars_weather = results.text.split("pic")
    mars_weather = p_mars_weather[0].strip()

    twitter = {"mars_weather": mars_weather}

    return twitter 

def mars_table(browser):
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts = tables[0]
    mars_facts = mars_facts.rename(columns={0:"Mars Characteristic", 1:"Fact"})
    mars_facts = mars_facts.set_index(["Mars Characteristic", "Fact"])
    # put table into html code
    mars_facts_html = mars_facts.to_html()
    # save to file
    marsfactstable = mars_facts.to_html('marsfactstable.html')
    print(marsfactstable)

    table = {"mars_table": marsfactstable}
    print(table)

    return table