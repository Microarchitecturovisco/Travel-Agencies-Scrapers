from initalize_scraper import init_webdriver
from scrapping_tours_urls import scrape_all_inclusive_tours
from scrapping_single_tour import scrape_single_tour

if __name__ == "__main__":
    driver = init_webdriver()

    tours_list = scrape_all_inclusive_tours(driver)

    for tour in tours_list:
        scrape_single_tour(driver, tour)

    # Close the browser
    driver.quit()
