from requests import get
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pprint
import json
from chewy_functions import *

def GetLinks(url, links, count = 0, stop = 1):
    while True:
            try:
                print(f"Trying {url}")
                page = get(url, timeout=5, headers={'User-Agent': 'SomeAgent 1.0'})
                soup = BeautifulSoup(page.content, 'html.parser')
                print(f"Success")
            except:
                print(f"Failed. Trying again: {url}")
                continue
            break

    result_count = soup.find('p', {"class": "results-count kib-typography-paragraph1 kib-breakpoint-hide@xs kib-breakpoint-hide@sm ProductListingGrid_resultsCount__3dRCX"}).text.split(" ")
    card_count_start= int(result_count[0])
    card_count_end = int(result_count[2]) 
    prod_count = int(result_count[4])

    cards = soup.find_all('div', {"class": "kib-product-card__content"})
    print(f"Product cards on this page: {card_count_start} - {card_count_end}")
    i = card_count_start
    for card in cards[0:card_count_end-card_count_start+1]:
        link = card.find('a', {"class": "kib-product-title"}).get('href')
        links.append(link)
        print(f"{i}: {link}")
        i += 1
        
    if i < prod_count:
        next_link = "https://www.chewy.com" + soup.find('a', {"class":"kib-pagination-new-item kib-pagination-new-item--interactive kib-pagination-new-item--next"}).get('href')
        print(f"Next page: {next_link}")
        GetLinks(next_link, links)
    else:
        print(f"No more pages.")
        SaveLinks(links, "chewy\chewy_links_test.txt")
        


url = "https://www.chewy.com/b/dry-food-294"
links = []

GetLinks(url, links)
#SaveLinks(links, "chewy_links_test.txt")

#with open("chewy\dry-food-output.html", "w", encoding = 'utf-8') as file:
    
#    # prettify the soup object and convert it into a string  
#    file.write(str(soup.prettify()))