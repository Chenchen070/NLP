from requests import get
from bs4 import BeautifulSoup
import os
import re
import pandas as pd

def get_blog_articles():
    websites = []
    urls = ['https://codeup.com/tips-for-prospective-students/mental-health-first-aid-training/',
            'https://codeup.com/featured/5-reasons-to-attend-our-new-cloud-administration-program/',
            'https://codeup.com/data-science/jobs-after-a-coding-bootcamp-part-1-data-science/',
            'https://codeup.com/featured/what-jobs-can-you-get-after-a-coding-bootcamp-part-2-cloud-administration/',
            'https://codeup.com/codeup-news/codeup-tv-commercial/']
    for x in urls:
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(x, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.text
        text = soup.find('div', id='main-content').text
        date = soup.select('span.published')[0].text
        websites.append({"title": title, "content": text, "date_published": date})
    return websites

def get_one_news():
    news = []
    url = ['https://inshorts.com/en/news/cancelling-ac-firstclass-confirmed-train-tickets-to-now-attract-5-gst-1661858617350']
    for x in url:
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(x, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('span', itemprop = 'headline').text
        body = soup.find('div', itemprop = 'articleBody').text
        author = soup.find('span', class_ = 'author').text
        date = soup.find("span", class_="time")["content"]
        news.append({"title": title, "content": body, "author": author, "date": date})
    return news

def get_url(topic):
    url = f"https://inshorts.com/en/read/{topic}"
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = []
    # Find all links within that topic
    for link in soup.find_all("a", href=True):
        urls.append(link["href"])
        lines = pd.Series(urls)
        urls = lines[lines.str.contains(r"^/en/news")].tolist()
        new_urls = []
        for i in urls:
            new_urls.append("https://inshorts.com" + i)
    return new_urls

def get_news_info(new_urls, topic):
    news = []
    for new_url in new_urls:
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(new_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('span', itemprop = 'headline').text
        body = soup.find('div', itemprop = 'articleBody').text
        author = soup.find('span', class_ = 'author').text
        date = soup.find("span", class_="time")["content"]
        news.append({"title": title, "content": body, "author": author, "date": date, 'category': topic})
    return news

def get_all_news(topics = []):
    all_news = []
    for topic in topics:
        new_urls = get_url(topic)
        news = get_news_info(new_urls, topic)
        all_news.append(news)
    all_news = sum(all_news, [])
    return pd.DataFrame(all_news)