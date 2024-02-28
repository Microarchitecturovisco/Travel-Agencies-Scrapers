from selenium.webdriver.common.by import By
from initalize_scraper import init_webdriver
from tour_class import Tour


def scrape_element_by_xpath(driver, element_xpath):
    element = driver.find_element(By.XPATH, element_xpath)
    element_value = element.text
    return element_value


def get_tour_name(driver):
    name_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[1]/div[2]/div[3]/span/span[2]/span[1]/span[2]"
    name = scrape_element_by_xpath(driver, name_xpath)
    return name


def get_tour_country(driver):
    country_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[2]/div/span/span[2]/div[2]/ul/li[3]/a"
    country = scrape_element_by_xpath(driver, country_xpath)
    return country


def get_tour_city(driver):
    city_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[2]/div/span/span[2]/div[2]/ul/li[4]/a"
    city = scrape_element_by_xpath(driver, city_xpath)
    return city


def get_tour_food_options(driver):
    food_options_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[1]/div[13]/div/section/span"
    element = driver.find_element(By.XPATH, food_options_xpath)

    # Finding all the list items (food options)
    food_options_element = element.find_elements(By.CLASS_NAME, "styles_c__features--expanded__9hNlD")

    food_options = []
    # Looping through each food option to extract its name and price
    for option in food_options_element:
        # Extracting the name of the food option
        name = option.find_element(By.CLASS_NAME, "styles_c__children__MR8TP").text
        food_options.append(name)
    return food_options


def get_restaurant_details(driver):
    details_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[1]/div[13]/div/section/span/span[2]/div/div[1]"
    restaurant_details = scrape_element_by_xpath(driver, details_xpath)
    return restaurant_details


def scrape_single_tour(driver, tour):
    driver.get(tour.link)
    driver.implicitly_wait(1)

    tour.name = get_tour_name(driver)
    tour.country = get_tour_country(driver)
    tour.city = get_tour_city(driver)
    tour.restaurant_details = get_restaurant_details(driver)
    tour.food_options = get_tour_food_options(driver)

    return tour


if __name__ == "__main__":
    driver = init_webdriver()
    test_tour_link = "https://www.itaka.pl/wczasy/zjednoczone-emiraty-arabskie/abu-dhabi/hotel-khalidiya-palace-rayhaan-by-rotana,AAEAUH1WKO.html?id=CgVJdGFrYRIEVklUWBoDUExOIgpBQUVBVUgxV0tPKAQ6BEtMMjBCBgiAkeizBkoGCICd%252FbMGUAJiBQoDS1JLagUKA0FVSHIICgZEUDMwMDh6BQoDQVVIggEFCgNLUkuKAQgKBkRQMzAwOJIBBgiAkeizBpoBBgiAnf2zBqIBDAoKUk1TRDAwMDBCMKoBAwoBQQ%253D%253D&participants%5B0%5D%5Badults%5D=2"
    test_tour = Tour(test_tour_link)
    test_tour = scrape_single_tour(driver, test_tour)

    # Close the browser
    driver.quit()
