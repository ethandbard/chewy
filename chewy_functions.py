from requests import get
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pprint
import json

# these items can be imported from chewy_functions
prod_links = []
prod_dict = {}

# get links from chewy.com dry dog food page
# https://www.chewy.com/b/dry-food-294
def get_links(url, links, count=0, stop=1):
    while True:
        try:
            # try to get page
            print(f"Trying {url}")
            # request page
            page = get(url, timeout=5, headers={"User-Agent": "SomeAgent 1.0"})
            # parse page
            soup = BeautifulSoup(page.content, "html.parser")
            print(f"Success")
        except:
            print(f"Failed. Trying again: {url}")
            continue
        break

    result_count = soup.find(
        "p",
        {
            "class": "results-count kib-typography-paragraph1 kib-breakpoint-hide@xs kib-breakpoint-hide@sm ProductListingGrid_resultsCount__ovDYA"
        },
    ).text.split(" ")
    card_count_start = int(result_count[0])
    card_count_end = int(result_count[2])
    prod_count = int(result_count[4])
    print(f"Product cards on this page: {card_count_start} - {card_count_end}")

    cards = soup.find_all("a", class_="kib-product-title")
    i = card_count_start
    for card in cards:
        if card["href"].startswith("https://www.chewy.com/"):
            print(card["href"])
            links.append(card["href"])
            i += 1

    if i < prod_count:
        next_link = "https://www.chewy.com" + soup.find(
            "a",
            {
                "class": "kib-pagination-new-item kib-pagination-new-item--interactive kib-pagination-new-item--next"
            },
        ).get("href")
        print(f"Next page: {next_link}")
        get_links(next_link, links)
    else:
        print(f"No more pages.")
        save_links(links)
        print("Links saved to file.")


# save links to file.
# this function is called by get_links() when all links have been scraped.
def save_links(links):
    textFile = open("chewy_links_9-23.txt", "w")

    for link in links:
        textFile.write(link + "\n")

    textFile.close()


def load_links(file):
    with open(file, "r") as f:
        for line in f:
            url = line.strip()
            prod_links.append(url)


def scrape_page(link):
    try:
        print(f"Trying: {link}")
        page = requests.get(
            link.rstrip(), timeout=5, headers={"User-Agent": "SomeAgent 1.0"}
        )
        print("Got Page\n")
        soup = BeautifulSoup(page.content, "html.parser")
        prod_name = soup.find("div", class_="styles_root__jNMr3").find("h1").text
        print(prod_name)

        # create dict
        specifications_dict = {}

        # get data
        specifications = (
            soup.find("div", class_="styles_infoGroupSectionTitle__cyv_p")
            .find_next_sibling("div")
            .find("table")
            .find_all("tr")
        )
        for i in range(0, len(specifications)):
            specifications_dict[specifications[i].find("th").text] = (
                specifications[i].find("td").text
            )
        prod_dict[specifications_dict["Item Number"]] = specifications_dict
        specifications_dict["name"] = prod_name

        # check for ingredients
        ingredients = soup.find("section", id="INGREDIENTS-section")
        if ingredients is not None:
            ingredients = ingredients.find("p")
            specifications_dict["Ingredients"] = ingredients.text

        # check for reccomendations/reviews
        rec_rate = soup.find("div", {"data-testid": "product-recommendation-rate"})
        if rec_rate is not None:
            rec_rate = rec_rate.find("div").text.replace("%", "")
            rating = soup.find("div", {"data-testid": "product-reviews-rating"}).text
            review_count = soup.find(
                "div", {"data-testid": "product-reviews-count"}
            ).text.split(" ")[0]
            specifications_dict["Reccomendation Rate"] = int(rec_rate)
            specifications_dict["Rating"] = float(rating)
            specifications_dict["Review Count"] = int(review_count)

        return True
    except:
        print(f"failed. Trying again: {link}")
        sleep(5)
        return False


def scrape_pages(links):
    for link in links:
        while not scrape_page(link):
            pass


def save_json(json, filename):
    with open(filename, "w") as outfile:
        outfile.write(json)


def load_json(filename):
    f = open(filename)
    json_data = json.load(f)
    f.close()
    return json_data
