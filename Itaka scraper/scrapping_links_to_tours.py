from selenium.webdriver.common.by import By
from tour_class import Tour


def scrape_all_inclusive_tours(driver):
    pages_to_check = 4
    tours = []
    for pg in range(1, pages_to_check + 1):
        website_link = "https://www.itaka.pl/all-inclusive/?page=" + str(pg)
        driver.get(website_link)

        load_whole_page(driver)  # scroll to the end of page

        # find all tours on the page
        tours_on_website = driver.find_elements(By.CLASS_NAME, "styles_c--secondary__93kD2")[1:-1]

        # save all tours
        for tour in tours_on_website:
            tour_web_link = tour.get_attribute('href')
            new_tour = Tour(tour_web_link)
            tours.append(new_tour)

    return tours


def load_whole_page(driver):
    # Scroll gradually to the end of page in several steps
    steps = 3
    wait_for_sec = 0.1
    for i in range(steps):
        driver.execute_script("window.scrollTo(0, " + str(i) + " * document.body.scrollHeight / " + str(steps) + " );")
        # driver.implicitly_wait(wait_for_sec)
