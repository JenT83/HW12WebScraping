from bs4 import BeautifulSoup
from splinter import Browser

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#ex need to customize for HW
def scrape():
    news = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news["news_title"] = soup.find('div', class_="content_title").text
    news["news_p"] = soup.find('div', class_="article_teaser_body").text

    return news

# Store data in a dictionary
    mars = {
        "news_title": news_title,
        "news_p": news_p,
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars