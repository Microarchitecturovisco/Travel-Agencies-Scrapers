from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Offer:

    def __init__(self, link):
        self.link = link


def init_webdriver():
    # Set up the Chrome webdriver (you need to have chromedriver installed)
    driver = webdriver.Chrome()
    # Navigate to the website
    driver.get("https://www.itaka.pl/")
    driver.implicitly_wait(2)
    return driver


def scrape_all_inclusive_offers():
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


def accept_cookies_button(driver):
    # Wait for the button to be clickable
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div[2]/button[3]")))

    # Click the "Accept cookies" button
    button.click()


def load_whole_page(driver):
    # Scroll gradually to the end of page in several steps
    steps = 10
    wait_for_sec = 0.1
    for i in range(steps):
        driver.execute_script("window.scrollTo(0, " + str(i) + " * document.body.scrollHeight / " + str(steps) + " );")
        # driver.implicitly_wait(wait_for_sec)


if __name__ == "__main__":
    driver = init_webdriver()

    accept_cookies_button(driver)

    all_inclusive_offers = scrape_all_inclusive_offers()

    # Close the browser
    driver.quit()
