from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_webdriver():
    # Set up the Chrome webdriver (you need to have chromedriver installed)
    driver = webdriver.Chrome()
    # Navigate to the website
    driver.get("https://www.itaka.pl/")
    driver.implicitly_wait(2)
    return driver


def scrape_all_inclusive_offers():
    website_link = "https://www.itaka.pl/all-inclusive/"
    driver.get(website_link)

    load_whole_page(driver)  # scroll to the end of page


    # "/html/body/div[5]/div[2]/div[6]/div[2]/div[1]/div/div[2]/div[2]/header/span[1]/span[2]/h5/a"
    # "/html/body/div[5]/div[2]/div[6]/div[26]/div[1]/div/div[2]/div[2]/header/span[1]/span[2]/h5/a"

    # for i in range(2, 27):
    #     link_element_xpath = "/html/body/div[5]/div[2]/div[6]/div[" + str(i) + "]/div[1]/div/div[2]/div[2]/header/span[1]/span[2]/h5/a"
    #     link_element = driver.find_element(By.XPATH, link_element_xpath)
    #     link = link_element.get_attribute("href")
    #     print("Link:", link)


def accept_cookies_button(driver):
    # Wait for the button to be clickable
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div[2]/button[3]")))

    # Click the button
    button.click()


def load_whole_page(driver):
    # Scroll gradually to the end of page in 10 steps
    for i in range(10):
        driver.execute_script("window.scrollTo(0, " + str(i) + " * document.body.scrollHeight / 10 );")
        driver.implicitly_wait(1)


if __name__ == "__main__":

    driver = init_webdriver()

    accept_cookies_button(driver)

    all_inclusive_offers = scrape_all_inclusive_offers()

    # Find all the article titles on the homepage
    article_titles = driver.find_elements(By.XPATH, "//h2[@class='article-title']")

    # Iterate over the article titles and print them
    for title in article_titles:
        print(title.text)

    # Close the browser
    driver.quit()

