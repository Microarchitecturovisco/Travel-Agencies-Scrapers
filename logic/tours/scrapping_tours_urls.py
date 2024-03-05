from selenium.webdriver.common.by import By
from tour_class import Tour


def scrape_all_inclusive_tours(driver):
    """
    Scrape all the all-inclusive tours from multiple pages on the website.

    This function navigates through multiple pages of all-inclusive tours,
    extracts tour urls, and creates Tour objects for each tour.

    Parameters:
    - driver: The Selenium WebDriver instance.

    Returns:
    - List[Tour]: A list of Tour objects representing the scraped tours.
    """
    try:
        pages_to_check = 2
        tours = []
        for pg in range(1, pages_to_check + 1):
            website_url = "https://www.itaka.pl/all-inclusive/?page=" + str(pg)
            driver.get(website_url)

            load_whole_page(driver)  # scroll to the end of page

            # find all tours on the page
            tours_on_website = driver.find_elements(By.CLASS_NAME, "styles_c--secondary__93kD2")[1:-1]

            # save all tours visible on this page
            for tour in tours_on_website:
                try:
                    tour_url = tour.get_attribute('href')
                    new_tour = Tour(tour_url)  # Assuming you have a Tour class to create Tour objects
                    tours.append(new_tour)
                except Exception as e:
                    print(f"An error occurred while processing a tour: {e}")

        return tours
    except Exception as e:
        print(f"An error occurred while scraping all-inclusive tours: {e}")
        return []

def load_whole_page(driver):
    """
    Scroll gradually to the end of the page in several steps.

    This function is used to simulate scrolling to the end of the page
    to ensure all elements are loaded before extracting data.

    Parameters:
    - driver: The Selenium WebDriver instance.
    """
    # Scroll gradually to the end of page in several steps
    steps = 3
    wait_for_sec = 0.1
    for i in range(steps):
        driver.execute_script("window.scrollTo(0, " + str(i) + " * document.body.scrollHeight / " + str(steps) + " );")
        # driver.implicitly_wait(wait_for_sec)
