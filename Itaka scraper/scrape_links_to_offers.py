from selenium.webdriver.common.by import By
from offer_class import Offer


def scrape_all_inclusive_offers(driver):
    pages_to_check = 2
    offers = []
    for pg in range(1, pages_to_check + 1):
        website_link = "https://www.itaka.pl/all-inclusive/?page=" + str(pg)
        driver.get(website_link)

        load_whole_page(driver)  # scroll to the end of page

        # find all offers on the page
        offers_on_website = driver.find_elements(By.CLASS_NAME, "styles_c--secondary__93kD2")[1:-1]

        # save all offers
        for offer in offers_on_website:
            offer_web_link = offer.get_attribute('href')
            new_offer = Offer(offer_web_link)
            offers.append(new_offer)

    return offers


def load_whole_page(driver):
    # Scroll gradually to the end of page in several steps
    steps = 5
    wait_for_sec = 0.1
    for i in range(steps):
        driver.execute_script("window.scrollTo(0, " + str(i) + " * document.body.scrollHeight / " + str(steps) + " );")
        # driver.implicitly_wait(wait_for_sec)
