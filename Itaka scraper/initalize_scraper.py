from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_webdriver():
    """
    Initialize a Chrome WebDriver and navigate to the website.

    Returns:
    - webdriver.Chrome: The initialized Chrome WebDriver.
    """
    # Set up the Chrome webdriver (you need to have chromedriver installed)
    driver = webdriver.Chrome()
    # Navigate to the website
    driver.get("https://www.itaka.pl/")
    driver.implicitly_wait(2)

    accept_cookies_button(driver)

    return driver


def accept_cookies_button(driver):
    """
    Clicks the "Accept cookies" button on the website.

    Parameters:
    - driver: The Selenium WebDriver instance.
    """
    accept_cookies_button_xpath = "/html/body/div[3]/div/div/div/div[2]/button[3]"
    # Wait for the button to be clickable
    waiting_time = 10  # seconds
    button = WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.XPATH, accept_cookies_button_xpath)))

    # Click the "Accept cookies" button
    button.click()
