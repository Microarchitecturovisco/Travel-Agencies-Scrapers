import re
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional, List
from logic.initalize_scraper import init_webdriver
from logic.tours.tour_class import Tour
from logic.tours.room_class import Room


def scrape_element_by_xpath(driver: WebDriver, element_xpath: str) -> Optional[str]:
    """Scrapes the text of the element located by XPath.

    Parameters:
    - driver (WebDriver): The WebDriver instance.
    - element_xpath (str): The XPath of the element.

    Returns:
    - Optional[str]: The text of the element if found, else None.
    """
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        element_value = element.text
        return element_value
    except NoSuchElementException:
        return None


def get_tour_name(driver: WebDriver) -> Optional[str]:
    """
    Get the name of the tour from the webpage.

    Parameters:
    - driver (WebDriver): The WebDriver object.

    Returns:
    - str or None: The name of the tour if found, else None.
    """
    try:
        element = driver.find_element(By.CLASS_NAME, "styles_c--with-spaces__KUJpZ")
        name = element.text
        return name
    except NoSuchElementException:
        return None


def get_tour_country(driver: WebDriver) -> Optional[str]:
    """
    Get the country of the tour from the webpage.

    Parameters:
    - driver (WebDriver): The WebDriver object.

    Returns:
    - str or None: The country of the tour if found, else None.
    """
    country_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[2]/div/span/span[2]/div[2]/ul/li[3]/a"
    country = scrape_element_by_xpath(driver, country_xpath)
    return country


def get_tour_city(driver: WebDriver) -> Optional[str]:
    """
    Get the city of the tour from the webpage.

    Parameters:
    - driver (WebDriver): The WebDriver object.

    Returns:
    - str or None: The city of the tour if found, else None.
    """
    city_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[2]/div/span/span[2]/div[2]/ul/li[4]/a"
    city = scrape_element_by_xpath(driver, city_xpath)
    return city


def get_tour_catering_options(driver: WebDriver) -> List[str]:
    """
    Get the catering options available for the tour from the webpage.

    If there is more than one option to choose, the button is clickable (enabled)
    and catering options are listed in a dropdown list.

    Parameters:
    - driver (WebDriver): The WebDriver object.

    Returns:
    - List[str]: A list of catering options available for the tour.
    """
    try:
        catering_options_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[2]/div/div/div[3]/div[4]/button"
        button_element = driver.find_element(By.XPATH, catering_options_xpath)

        if button_element.is_enabled():  # more than one option available - open dropdown list
            button_element.click()  # open dropdown list
            driver.implicitly_wait(2)

            catering_options = get_catering_options_from_dropdown_list(driver)

            button_element.click()  # close dropdown list

            return catering_options

        else:  # only one option available
            button_text = button_element.text
            catering_options = button_text.split("\n")[1:]

        return catering_options
    except Exception as e:
        print(f"An error occurred while getting tour catering options: {e}")
        return []


def get_catering_options_from_dropdown_list(driver: WebDriver):
    """
    Extracts catering options from the dropdown list on the Itaka website.

    Parameters:
    - driver: The Selenium WebDriver instance.

    Returns:
    - list: A list of catering option names extracted from the dropdown list.
    """
    try:
        # Find all elements within the catering options list
        catering_opt_elements = driver.find_elements(By.CLASS_NAME, "styles_c__h83a9")
        catering_options = []
        # Iterate over each element to extract catering option names
        for element in catering_opt_elements:
            try:
                catering_opt_name = element.text.split("\n")[0]
                catering_options.append(catering_opt_name)
            except Exception as e:
                print(f"An error occurred while extracting catering option name: {e}")
        return catering_options
    except Exception as e:
        print(f"An error occurred while getting catering options: {e}")
        return []


def get_tour_photos(driver: WebDriver) -> List[str]:
    """
    Get the URLs of photos related to the tour from the webpage.

    Parameters:
    - driver (WebDriver): The WebDriver object.

    Returns:
    - List[str]: A list of URLs of photos related to the tour.
    """
    try:
        # XPath to locate the parent <ul> element containing the images
        photos_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[1]/div[1]/div/div[3]/div[4]/ul"
        element = driver.find_element(By.XPATH, photos_xpath)

        photo_elements = element.find_elements(By.TAG_NAME, "li")

        image_urls = []

        # Looping through each <li> element to extract the image URLs
        for element in photo_elements:
            try:
                # Finding the <img> element within the <li> element
                img_element = element.find_element(By.TAG_NAME, "img")
                image_url = img_element.get_attribute("src")
                image_urls.append(image_url)
            except Exception as e:
                print(f"An error occurred while extracting image URL: {e}")

        return image_urls
    except Exception as e:
        print(f"An error occurred while getting tour photos: {e}")
        return []



def get_room_options(driver: WebDriver):
    rooms = []
    person_button = driver.find_element(By.XPATH, "//*[@class='styles_c__Muqrv styles_wrapper__1Wod9']/button[2]")
    person_button.click()
    time.sleep(1)
    sub_person_button = driver.find_element(By.XPATH, "//button[@class='styles_c__VNmM2 "
                                                      "styles_c--secondary__oM3BG'][1]")
    while sub_person_button.is_enabled():
        sub_person_button.click()
        time.sleep(1)

    save_person_button = driver.find_element(By.XPATH, "//*[@class='ps-3 ms-auto']/button")
    save_person_button.click()
    room_capacity = 1
    while True:
        time.sleep(1)
        try:
            rooms_div = driver.find_element(By.NAME, "rooms")
        except NoSuchElementException:
            break

        all_rooms = rooms_div.find_elements(By.CLASS_NAME, "col-md-6")
        price_div = driver.find_element(By.XPATH, '//*[@data-testid="current-price"]/span[1]').text.strip()
        standard_price = price_div.replace(" ", "").replace("zł", "")

        for room in all_rooms:
            new_room = Room()
            room_name = room.find_element(By.TAG_NAME, "h4").text.strip()
            room_button = room.find_element(By.XPATH, ".//ul/button")
            room_button.click()
            room_descriptions = room.find_elements(By.XPATH, ".//li/span/span[2]")
            room_description = ',  '.join([description.text for description in room_descriptions])

            price_div = room.find_element(By.XPATH, './/*[@class="styles_price__XJaTa styles_price--with-bottom-'
                                                    'space__CFyLx"]/strong').text.strip()
            room_price = 0
            if price_div == "w cenie":
                room_price = int(standard_price)
            else:
                additional_price = re.findall(r'\d+', price_div)
                additional_price = ''.join(additional_price)
                room_price = int(standard_price) + int(additional_price)

            new_room.name = room_name
            new_room.description = room_description
            new_room.price = room_price
            new_room.capacity = room_capacity
            rooms.append(new_room)

        driver.execute_script("window.scrollTo(0, 0);")
        person_button = driver.find_element(By.XPATH, "//*[@class='styles_c__Muqrv styles_wrapper__1Wod9']/button[2]")
        person_button.click()
        time.sleep(1)
        add_person_button = driver.find_element(By.XPATH, "//button[@class='styles_c__VNmM2 "
                                                          "styles_c--secondary__oM3BG'][2]")
        if not add_person_button.is_enabled():
            break
        add_person_button.click()
        room_capacity += 1
        save_person_button = driver.find_element(By.XPATH, "//*[@class='ps-3 ms-auto']/button")
        save_person_button.click()
    return rooms



def get_airport_options(driver: WebDriver) -> List[str]:
    """
    Get the airport options available for the tour from the webpage.

    If there is more than one option to choose, the button is clickable (enabled)
    and airport options are listed in a dropdown list.

    Parameters:
    - driver (WebDriver): The WebDriver object.

    Returns:
    - List[str]: A list of airport options available for the tour.
    """
    try:
        button_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[2]/div/div/div[3]/div[5]/button"
        button_element = driver.find_element(By.XPATH, button_xpath)

        if button_element.is_enabled():  # more than one option available - open dropdown list
            button_element.click()  # open dropdown list
            time.sleep(1)

            airport_cities = get_airport_options_from_dropdown_list(driver)

            button_element.click()  # close dropdown list

        else:  # only one option available
            button_value = button_element.text
            airport_cities = button_value.split("\n")[1:]

        return airport_cities
    except Exception as e:
        print(f"An error occurred while getting airport options: {e}")
        return []


def get_airport_options_from_dropdown_list(driver):
    """
    Extracts airport options from the dropdown list.

    Parameters:
    - driver: WebDriver instance

    Returns:
    - List[str]: List of airport cities
    """
    try:
        # Select the dropdown list element
        airport_opt_xpath = "/html/body/div[6]/div/div/div/div[1]"
        airport_opt_element = driver.find_element(By.XPATH, airport_opt_xpath)
        airport_cities = get_default_airport_options(airport_opt_element)
        get_additional_airport_options(airport_cities, airport_opt_element)
        airport_cities = [value.split('\n')[0] for value in airport_cities]  # Extract the city name
        return airport_cities
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_additional_airport_options(airport_cities: List[str], airport_opt_element: WebElement) -> None:
    """
    Extracts additional airport options from the given element and appends them to the list of airport cities.

    Parameters:
    - airport_cities (List[str]): The list of airport cities to which additional options will be appended.
    - airport_opt_element (WebElement): The WebElement containing additional airport options.

    Returns:
    - None
    """
    try:
        additional_list_xpath = "./div/ul/li[@class='styles_c__h83a9']"
        additional_airport_opt_elements = airport_opt_element.find_elements(By.XPATH, additional_list_xpath)
        for element in additional_airport_opt_elements:
            # Extracting the airport information
            label_element = element.find_element(By.CLASS_NAME, "styles_c__label__q3Tzc")
            airport_city = label_element.find_element(By.CLASS_NAME, "oui-font-size-14").text
            airport_cities.append(airport_city)
    except Exception as e:
        print(f"An error occurred: {e}")


def get_default_airport_options(airport_opt_element: WebElement) -> List[str]:
    """
    Extract default airport options from the given element.

    Parameters:
    - airport_opt_element (WebElement): The WebElement containing default airport options.

    Returns:
    - List[str]: A list of default airport cities.
    """
    airport_cities = []
    # Find all li elements within the ul
    li_elements = airport_opt_element.find_elements(By.XPATH, "./ul/li")
    # Iterate over each li element to extract city names
    for li_element in li_elements:
        city_name = li_element.find_element(By.XPATH, ".//span[contains(@class, 'oui-font-size-14')]").text
        airport_cities.append(city_name)

    return airport_cities


def scrape_single_tour(driver: WebDriver, tour: Tour) -> Tour:
    """Scrapes information about a single tour.

    Args:
        driver (WebDriver): The WebDriver instance.
        tour (Tour): The tour object to populate with scraped information.

    Returns:
        Tour: The tour object populated with scraped information.
    """
    print("tour url:")
    driver.get(tour.url)
    print(tour.url)
    driver.implicitly_wait(10)
    time.sleep(3)  # wait for the page to load

    tour.name = get_tour_name(driver)
    tour.country = get_tour_country(driver)
    tour.city = get_tour_city(driver)
    if tour.city is None:
        tour.city = tour.country
    tour.photos = get_tour_photos(driver)
    tour.airport_options = get_airport_options(driver)
    tour.catering_options = get_tour_catering_options(driver)
    rooms = get_room_options(driver)
    print("tour scrapped successfully\n")
    return tour


if __name__ == "__main__":
    driver = init_webdriver()
    # test_tour_url = "https://www.itaka.pl/wczasy/zjednoczone-emiraty-arabskie/abu-dhabi/hotel-khalidiya-palace-rayhaan-by-rotana,AAEAUH1WKO.html?id=CgVJdGFrYRIEVklUWBoDUExOIgpBQUVBVUgxV0tPKAQ6BEtMMjBCBgiAkeizBkoGCICd%252FbMGUAJiBQoDS1JLagUKA0FVSHIICgZEUDMwMDh6BQoDQVVIggEFCgNLUkuKAQgKBkRQMzAwOJIBBgiAkeizBpoBBgiAnf2zBqIBDAoKUk1TRDAwMDBCMKoBAwoBQQ%253D%253D&participants%5B0%5D%5Badults%5D=2"
    # test_tour_url = "https://www.itaka.pl/wczasy/kenia/twiga-beach-resort-and-spa,MBATWIG.html?id=CgVJdGFrYRIEVklUWBoDUExOIgdNQkFUV0lHKAQ6BEwwNjBCBgiAqqmvBkoGCICfzq8GUAJiBQoDV1JPagUKA01CQXIDCgExegUKA01CQYIBBQoDV1JPigEDCgExkgEGCICqqa8GmgEGCICfzq8GogEFCgNMU1aqAQMKAUE%253D"
    # test_tour_url = "https://www.itaka.pl/wczasy/tunezja/mahdia/hotel-thalassa-mahdia,NBETAMA.html"
    test_tour_url = "https://www.itaka.pl/wczasy/zjednoczone-emiraty-arabskie/abu-dhabi/hotel-khalidiya-palace-rayhaan-by-rotana,AAEAUH1WKO.html?id=CgVJdGFrYRIEVklUWBoDUExOIgpBQUVBVUgxV0tPKAQ6BEtMMjBCBgiAkeizBkoGCICd%252FbMGUAJiBQoDS1JLagUKA0FVSHIICgZEUDMwMDh6BQoDQVVIggEFCgNLUkuKAQgKBkRQMzAwOJIBBgiAkeizBpoBBgiAnf2zBqIBDAoKUk1TRDAwMDBCMKoBAwoBQQ%253D%253D&participants[0][adults]=2"
    test_tour = Tour(test_tour_url)
    test_tour = scrape_single_tour(driver, test_tour)

    # Close the browser
    driver.quit()
