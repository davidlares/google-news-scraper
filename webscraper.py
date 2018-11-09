from bs4 import BeautifulSoup
import requests
import threading
from pymongo import MongoClient

GOOGLE_NEWS_URL="https://news.google.com"

def set_robot(article, db):
    title = article.find('span').getText()
    url = article.find('a', {'class': 'ipQwMb Q7tWef'}).get('href')
    # generating schema
    json = {'title': title, 'url': url}
    # inserting in collection articles
    db.articles.insert_one(json)
    print "Article Added"

def scraping_site():
    re = requests.get(GOOGLE_NEWS_URL)
    if re.status_code == 200: # success request
        soup = BeautifulSoup(re.text, 'html.parser') # re.text -> html content
        if soup is not None:
            # mongo integration
            client = MongoClient('localhost', 27017) # local connection
            db = client.webscrapper #webscraper - database
            # find articles
            articles = soup.find_all('h3')
            for article in articles:
                robot = threading.Thread(name="set_robot", target=set_robot, args=(article,db))
                robot.start()
        else:
            print "Wrong Soup"
    else:
        print "Wrong request"

if __name__ == '__main__':
    scraping_site()
