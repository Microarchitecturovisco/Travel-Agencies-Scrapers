from logic.initalize_scraper import init_webdriver
from logic.tours.scrapping_tours_urls import scrape_all_inclusive_tours
from logic.tours.scrapping_single_tour import scrape_single_tour

if __name__ == "__main__":
    driver = init_webdriver()

    tours_urls = scrape_all_inclusive_tours(driver)

    tours_result = []

    for tour in tours_urls[:2]:  # TODO WIP, handle more urls
        tours_result.append(scrape_single_tour(driver, tour))

    # Close the browser
    driver.quit()
