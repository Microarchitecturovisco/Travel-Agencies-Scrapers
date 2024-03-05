from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_webdriver(webdriver_type: str = 'chrome'):
    """
    Initialize a Chrome WebDriver and navigate to the website.

    Parameters
    ----------
    webdriver_type
        Type of webdriver to use for scraping, either 'chrome' or 'firefox'

    Returns
    -------
    The initialized WebDriver.
    """
    # Set up the webdriver (you need to have chromedriver or firefox installed)
    driver = webdriver.Chrome() if webdriver_type == 'chrome' else webdriver.Firefox() if webdriver_type == 'firefox' else webdriver.Chrome()
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
