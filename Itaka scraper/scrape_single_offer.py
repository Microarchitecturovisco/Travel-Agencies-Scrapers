from selenium.webdriver.common.by import By
from initalize_scraper import init_webdriver
from offer_class import Offer

def scrape_element_by_xpath(driver, element_xpath):
    element = driver.find_element(By.XPATH, element_xpath)
    element_value = element.text
    return element_value

def get_offer_name(driver):
    name_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[1]/div[2]/div[3]/span/span[2]/span[1]/span[2]"
    name = scrape_element_by_xpath(driver, name_xpath)
    return name

def get_offer_country(driver):
    country_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[2]/div/span/span[2]/div[2]/ul/li[3]/a"
    country = scrape_element_by_xpath(driver, country_xpath)
    return country

def get_offer_city(driver):
    city_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[2]/div/span/span[2]/div[2]/ul/li[4]/a"
    city = scrape_element_by_xpath(driver, city_xpath)
    return city


def scrape_single_offer(driver, offer):
    driver.get(offer.link)
    driver.implicitly_wait(1)

    name = get_offer_name(driver)
    country = get_offer_country(driver)
    city = get_offer_city(driver)


if __name__ == "__main__":
    driver = init_webdriver()
    test_offer_link = "https://www.itaka.pl/wczasy/zjednoczone-emiraty-arabskie/abu-dhabi/hotel-khalidiya-palace-rayhaan-by-rotana,AAEAUH1WKO.html?id=CgVJdGFrYRIEVklUWBoDUExOIgpBQUVBVUgxV0tPKAQ6BEtMMjBCBgiAkeizBkoGCICd%252FbMGUAJiBQoDS1JLagUKA0FVSHIICgZEUDMwMDh6BQoDQVVIggEFCgNLUkuKAQgKBkRQMzAwOJIBBgiAkeizBpoBBgiAnf2zBqIBDAoKUk1TRDAwMDBCMKoBAwoBQQ%253D%253D&participants%5B0%5D%5Badults%5D=2"
    test_offer = Offer(test_offer_link)
    scrape_single_offer(driver, test_offer)

    # Close the browser
    driver.quit()
