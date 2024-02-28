from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from initalize_scraper import init_webdriver
from tour_class import Tour


def scrape_element_by_xpath(driver, element_xpath):
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        element_value = element.text
        return element_value
    except NoSuchElementException:
        return None


def get_tour_name(driver):
    element = driver.find_element(By.CLASS_NAME, "styles_c--with-spaces__KUJpZ")
    name = element.text
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
    food_options_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[2]/div/div/div[3]/div[4]/button"
    button_element = driver.find_element(By.XPATH, food_options_xpath)

    if button_element.is_enabled():
        button_element.click()
        driver.implicitly_wait(2)

        # Find all elements within the food options list
        food_opt_element = driver.find_elements(By.CLASS_NAME, "styles_c__h83a9")

        food_options = []

        # Iterate over each li element to extract food option names
        for element in food_opt_element:
            food_opt_name = element.text.split("\n")[0]
            food_options.append(food_opt_name)

        button_element.click()

        return food_options

    else:
        button_text = button_element.text
        food_options = button_text.split("\n")[1:]

    return food_options


def get_tour_photos(driver):
    # XPath to locate the parent <ul> element containing the images
    photos_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[1]/div[1]/div/div[3]/div[4]/ul"
    element = driver.find_element(By.XPATH, photos_xpath)

    # Finding all <li> elements under the parent <ul> element
    photo_items = element.find_elements(By.TAG_NAME, "li")

    # List to store image URLs
    image_urls = []

    # Looping through each <li> element to extract the image URLs
    for item in photo_items:
        # Finding the <img> element within the <li> element
        img_element = item.find_element(By.TAG_NAME, "img")

        # Extracting the 'src' attribute of the <img> element (image URL)
        image_url = img_element.get_attribute("src")

        # Appending the image URL to the list
        image_urls.append(image_url)

    return image_urls


def get_airport_options(driver):
    # Click the button to see airport options - list of airports
    button_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[2]/div/div/div[3]/div[5]/button"
    button_element = driver.find_element(By.XPATH, button_xpath)
    airport_cities = ""
    if button_element.is_enabled():
        button_element.click()
        driver.implicitly_wait(2)

        # select the dropdown list element
        airport_opt_xpath = "/html/body/div[6]/div/div/div/div[1]"
        airport_opt_element = driver.find_element(By.XPATH, airport_opt_xpath)

        airport_cities = get_default_airport_options(airport_opt_element)

        get_additional_airport_options(airport_cities, airport_opt_element)

        airport_cities = [value.split('\n')[0] for value in airport_cities]  # extract name only

        button_element.click()

    else:
        button_value = button_element.text
        airport_cities = button_value.split("\n")[1:]

    return airport_cities


def get_additional_airport_options(airport_cities, airport_opt_element):
    # Get values from the second longer list
    additional_airport_opt_elements = airport_opt_element.find_elements(By.XPATH,
                                                                        "./div/ul/li[@class='styles_c__h83a9']")
    for element in additional_airport_opt_elements:
        # Extracting the airport information
        label_element = element.find_element(By.CLASS_NAME, "styles_c__label__q3Tzc")
        # airport_info['city'] = label_element.find_element(By.CLASS_NAME, "oui-font-size-14").text
        # airport_info['date_time'] = label_element.find_element(By.TAG_NAME, "div").text
        # airport_info['price'] = element.find_element(By.CLASS_NAME, "text-nowrap").text
        airport_city = label_element.find_element(By.CLASS_NAME, "oui-font-size-14").text
        airport_cities.append(airport_city)


def get_default_airport_options(airport_opt_element):
    airport_cities = []
    # Find all li elements within the ul
    li_elements = airport_opt_element.find_elements(By.XPATH, "./ul/li")
    # Iterate over each li element to extract city names
    for li_element in li_elements:
        city_name = li_element.find_element(By.XPATH, ".//span[contains(@class, 'oui-font-size-14')]").text
        airport_cities.append(city_name)

    return airport_cities


def scrape_single_tour(driver, tour):
    print("tour link:")
    driver.get(tour.link)
    print(tour.link)
    driver.implicitly_wait(2)

    tour.name = get_tour_name(driver)
    tour.country = get_tour_country(driver)
    tour.city = get_tour_city(driver) or tour.country
    # tour.restaurant_details = get_restaurant_details(driver)
    tour.photos = get_tour_photos(driver)
    tour.airport_options = get_airport_options(driver)
    tour.food_options = get_tour_food_options(driver)
    print("tour scrapped successfully\n")
    return tour


if __name__ == "__main__":
    driver = init_webdriver()
    test_tour_link = "https://www.itaka.pl/wczasy/zjednoczone-emiraty-arabskie/abu-dhabi/hotel-khalidiya-palace-rayhaan-by-rotana,AAEAUH1WKO.html?id=CgVJdGFrYRIEVklUWBoDUExOIgpBQUVBVUgxV0tPKAQ6BEtMMjBCBgiAkeizBkoGCICd%252FbMGUAJiBQoDS1JLagUKA0FVSHIICgZEUDMwMDh6BQoDQVVIggEFCgNLUkuKAQgKBkRQMzAwOJIBBgiAkeizBpoBBgiAnf2zBqIBDAoKUk1TRDAwMDBCMKoBAwoBQQ%253D%253D&participants%5B0%5D%5Badults%5D=2"
    test_tour = Tour(test_tour_link)
    test_tour = scrape_single_tour(driver, test_tour)

    # Close the browser
    driver.quit()
