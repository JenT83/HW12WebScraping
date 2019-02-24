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
    hemi = mars_hemi(browser)

    browser.quit()

    # Return results
    data = {"news": news,
    "fi": fi,
    "mtw": mtw,
    "table": table,
    "hemi": hemi}   

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

    twitter = soup.find_all('div', class_="js-tweet-text-container")
    for tweet in reversed(twitter):
        if tweet.p.text.split(' ')[0] == "InSight":
            p_mars_weather = tweet.p.text.split("pic")
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
    table = {}
    table["mars_table"]= mars_facts_html

    return table

def mars_hemi(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    marshemi = []
    astro = soup.find_all('div', class_="description")
    links = browser.find_by_css("a.product-item h3")
        
    for i in range(len(links)):
        browser.find_by_css("a.product-item h3")[i].click()
        sample_elem = browser.find_link_by_text('Sample').first
        href = sample_elem['href']
        title = browser.find_by_css("h2.title").text
        marshemi.append({
        "link": href,
        "title": title})
        browser.back()

    return marshemi