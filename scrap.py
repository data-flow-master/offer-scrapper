import requests
from bs4 import BeautifulSoup
import time
import pprint


def scrape_offer(offer):
    offer_title = offer\
        .find("div",
              attrs={"data-cy": "ad-card-title"})\
        .find("a")
    offer_price = offer\
        .find("p",
              attrs={"data-testid": "ad-price"})

    offer_price_span = offer_price\
        .find("span")
    if offer_price_span:
        offer_price_span.replaceWith("")

    offer_location = offer\
        .find("p",
              attrs={"data-testid": "location-date"})
    offer_year_and_mileage = offer\
        .find("div",
              attrs={"color": "text-global-secondary"})\
        .find("span")\
        .find("span")

    if all([offer_title, offer_price, offer_location, offer_year_and_mileage]):
        return {
            "title": offer_title.get_text(),
            "price": offer_price.get_text(),
            "location": offer_location.get_text().split("-")[0].strip(),
            "year": offer_year_and_mileage.get_text().split("-")[0].strip(),
            "mileage": offer_year_and_mileage.get_text().split("-")[-1].strip()
        }
    else:
        return dict()


def scrape_offers_from_page(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    offers = soup.find_all("div",
                           attrs={"data-cy": "l-card"})

    if offers:
        for offer in offers:
            data = scrape_offer(offer)
            print(pprint.pformat(data))


def scrape_offers(url_template, page_from, page_to):
    for pn in range(page_from, page_to):
        scrape_offers_from_page(
            url_template.format(pn))
        time.sleep(1)


if __name__ == "__main__":
    URL_TEMPLATE = "https://www.olx.pl/motoryzacja/samochody/?page={}"
    PAGE_FROM = 1
    PAGE_TO = 2

    scrape_offers(
        URL_TEMPLATE,
        PAGE_FROM,
        PAGE_TO)
