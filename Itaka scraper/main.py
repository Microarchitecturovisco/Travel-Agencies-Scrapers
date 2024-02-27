from initalize_scraper import init_webdriver
from scrape_links_to_offers import scrape_all_inclusive_offers
from scrape_single_offer import scrape_single_offer

if __name__ == "__main__":
    driver = init_webdriver()

    offers_list = scrape_all_inclusive_offers(driver)

    for offer in offers_list:
        scrape_single_offer(offer)

    # Close the browser
    driver.quit()
