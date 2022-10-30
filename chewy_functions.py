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
    while True:
        try:
            print(f"Trying {url}")
            page = get(url, timeout=5, headers={'User-Agent': 'SomeAgent 1.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find('div', class_="results-content")
            print(f"Success")
        except:
            print(f"Failed. Trying again: {url}")
            continue
        break
    
        print(f"")
        paginator = results.find(
            'section', class_="cw-pagination results-pagination")
        articles = results.find_all(
            'article', class_="product-holder js-tracked-product cw-card cw-card-hover")
        
    while True:
        try:
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
        except:
            continue
        break


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


def ScrapePages(links):
    counter = 1
    for link in links:
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
                
                #check for ingredients
                ingredients = soup.find('section', id="INGREDIENTS-section")
                if ingredients is not None:
                    ingredients = ingredients.find('p')
                    specifications_dict['Ingredients'] = ingredients.text
                
                #check for reccomendations/reviews
                rec_rate = soup.find('div', {"data-testid": "product-recommendation-rate"})
                if rec_rate is not None:
                    rec_rate = rec_rate.find('div').text.replace("%","")
                    rating = soup.find('div', {"data-testid": "product-reviews-rating"}).text
                    review_count = soup.find('div',{"data-testid": "product-reviews-count"}).text.split(" ")[0]
                    specifications_dict['Reccomendation Rate'] = int(rec_rate)
                    specifications_dict['Rating'] = float(rating)
                    specifications_dict['Review Count'] = int(review_count)
                
                #add specifications to dict
                for i in range(0, len(specifications)):
                    specifications_dict[specifications[i].find('th').text] = specifications[i].find('td').text
                prod_dict[specifications_dict['Item Number']] = specifications_dict
                print(f"Success ({counter} / {len(prod_links)})")
                counter += 1
            except:
                print(f"failed. Trying again: {link}")
                sleep(5)
                continue
            break
        
 
def WriteJson(filename):
    with open(filename, "w") as outfile:
        outfile.write(prod_json)
        

