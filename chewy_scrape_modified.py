from requests import get
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint

prod_names = []
prod_made_in = []
prod_analysis = []
prod_ingredients = []
prod_links = []

# Product Attributes
Grain_Free = []
Pork = []
Rabbit = []
Beef = []
Chicken = []
Fish = []
Lamb = []
Egg = []
Corn = []
Soy = []
Wheat = []
Dairy = []

found = 0
notFound = 0


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
    counter = 1
    for page in pages:
        print(f"Scraping page ({counter}/{len(prod_links)})")
        counter += 1
        url = page
        while url == page:
            try:
                print(page)
                bowl = requests.get(page.rstrip(),
                                    timeout=5, headers={'User-Agent': 'SomeAgent 1.0'})
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

        soup = BeautifulSoup(bowl.content, 'html.parser')
        soup_2 = soup.find('article', id="Nutritional-Info")
        nutrition_container = soup_2.find(
            'section', class_="cw-tabs__content--left")
        nutrition = nutrition_container.find_all('p')

        print(nutrition[0].get_text().strip().split()[0])


# populates prod_links from textfile
LoadLinks("chewy\chewyLinks.txt")


for page in prod_links:
    try:
        print(f"Trying: {prod_links[1]}")
        page = requests.get(prod_links[1].rstrip(),
                            timeout=5, headers={'User-Agent': 'SomeAgent 1.0'})
        print("success")
        soup = BeautifulSoup(page.content, 'html.parser')
        print(soup.find('section', id="INGREDIENTS-section").find('p'))
        break
    except:
        #print("Connection refused by the server..")
        #print("Let me sleep for 5 seconds")
        #print("ZZzzzz...")
        sleep(5)
        #print("Was a nice sleep, now let me continue...")
        continue

#ScrapePages(prod_links)
       


# GetLinks("https://www.chewy.com/b/dry-food-294")
# SaveLinks(prod_links)

# ScrapePages(prod_links[:30])

# ingredient_catalog = {'Names': prod_names[:35],
# 'Ingredients': prod_ingredients}

# product_data = {
#     'Product_Name': prod_names[:30],
#     'Price': "NULL",
#     'Grain_Free': Grain_Free[:30],
#     'Chicken': Chicken,
#     'Beef': Beef,
#     'Fish': Fish,
#     'Pork': Pork,
#     'Rabbit': Rabbit,
#     'Lamb': Lamb,
#     'Egg': Egg,
#     'Corn': Corn,
#     'Soy': Soy,
#     'Wheat': Wheat,
#     'Dairy': Dairy}

# product_data_df = pd.DataFrame(product_data)
# product_data_df.to_csv('Product Attributes.csv')

# ingredients_catalog_df = pd.DataFrame(ingredient_catalog)
# print(ingredients_catalog_df)
# ingredients_catalog_df.to_csv('chewy scrape.csv')
