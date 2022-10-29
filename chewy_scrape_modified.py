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


def SaveLinks(links):
    textFile = open("chewyLinks.txt", 'w')

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

        # if 'Chicken' in ingredients:
        #     Chicken.append("1")
        # else:
        #     Chicken.append("0")

        # if "Pork" in ingredients:
        #     Pork.append("1")
        # else:
        #     Pork.append('0')

        # if 'Beef' in ingredients:
        #     Beef.append('1')
        # else:
        #     Beef.append('0')

        # if 'Rabbit' in ingredients:
        #     Rabbit.append('1')
        # else:
        #     Rabbit.append('0')

        # if 'Salmon' or 'Tuna' or 'fish' in ingredients:
        #     Fish.append('1')
        # else:
        #     Fish.append('0')

        # if 'Lamb' in ingredients:
        #     Lamb.append('1')
        # else:
        #     Lamb.append('0')

        # if 'Egg' in ingredients:
        #     Egg.append('1')
        # else:
        #     Egg.append('0')

        # if 'Corn' in ingredients:
        #     Corn.append('1')
        # else:
        #     Corn.append('0')

        # if 'Soy' in ingredients:
        #     Soy.append('1')
        # else:
        #     Soy.append('0')

        # if 'Wheat' in ingredients:
        #     Wheat.append('1')
        # else:
        #     Wheat.append('0')

        # if 'Cheese' or 'Cream' in ingredients:
        #     Dairy.append('1')
        # else:
        #     Dairy.append('0')

        # if len(nutrition) > 2:
        # .replace("Contains A Source Of Live (Viable), Naturally Occurring Microorganisms.", "").replace(
        # ingredients = nutrition[1].get_text()
        # "Ingredient Statement:", "").replace("New Formulation:", "").replace("New Formula:", "").strip()
        # else:
        # .replace("Contains A Source Of Live (Viable), Naturally Occurring Microorganisms.", "").replace(
        # ingredients = nutrition[0].get_text()
        #  "Ingredient Statement:", "").strip()

        # print(ingredients)
        # prod_ingredients.append(ingredients)


# populates prod_links from textfile
LoadLinks("Python Scripts\chewyLinks.txt")
ScrapePages(prod_links)


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
