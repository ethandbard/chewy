from requests import get
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pprint
import json

prod_links = []
prod_dict = {}


def GetLinks(url):
    page = get(url, timeout=5, headers={'User-Agent': 'SomeAgent 1.0'})
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_="results-content")
    paginator = results.find(
        'section', class_="cw-pagination results-pagination")
    articles = results.find_all(
        'article', class_="product-holder js-tracked-product cw-card cw-card-hover")
    for article in articles:
        data_name = article.get('data-name')
        prod_names.append(data_name)
        prod_holder = article.find('a')
        link = prod_holder.get('href')
        prod_links.append(link)
        # price = prod_holder.find_all('p', class_="price")
        if 'Grain-Free' in data_name:
            Grain_Free.append('1')
        else:
            Grain_Free.append('0')

    if paginator.find('a', class_="cw-pagination__next") is not None:
        next_page = paginator.find('a', class_="cw-pagination__next")
        print(f"Got next page: {next_page.get('href')}")
        GetLinks("https://www.chewy.com" + next_page.get('href'))


def SaveLinks(links, filename):
    textFile = open(filename, 'w')

    for link in links:
        textFile.write(link + '\n')

    textFile.close()


def LoadLinks(file):
    textFile = open(file, "r")
    for line in textFile.readlines():
        prod_links.append(line)
    textFile.close()


def ScrapePages(pages):
    for link in prod_links[0:2]:
        while True:
            try:
                print(f"Trying: {link}")
                page = requests.get(link.rstrip(),
                                    timeout=5, headers={'User-Agent': 'SomeAgent 1.0'})
                soup = BeautifulSoup(page.content, 'html.parser')
                prod_name = soup.find("div", {"class": "_2lMe8l0Qayns-EKWOOJfXh"}).find('h1').text
                print(prod_name)
                specifications = soup.find('div', {"class": "_3xer4bkNDgAik73jS-7m94"}).find('table').find_all('tr')
                specifications_dict = {}
                specifications_dict['name'] = prod_name
                specifications_dict['Ingredients'] = soup.find('section', id="INGREDIENTS-section").find('p').text 
                for i in range(0, len(specifications)):
                    specifications_dict[specifications[i].find('th').text] = specifications[i].find('td').text
                prod_dict[specifications_dict['Item Number']] = specifications_dict
                print("success")
            except:
                print(f"failed. Trying again: {link}")
                sleep(5)
                continue
            break
        
        
# populates prod_links from textfile
LoadLinks("chewy\chewyLinks.txt")

ScrapePages(prod_links)

prod_json = json.dumps(prod_dict, indent = 4)
pprint.pprint(prod_dict)

with open("chewy\sample.json", "w") as outfile:
    outfile.write(prod_json)
