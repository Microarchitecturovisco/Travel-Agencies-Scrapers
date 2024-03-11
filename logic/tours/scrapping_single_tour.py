import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional, List
from logic.initalize_scraper import init_webdriver
from logic.tours.tour_class import Tour


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


def get_tour_rating(driver: WebDriver) -> Optional[str]:
    return scrape_element_by_xpath(driver, '(//*[@data-testid="reviews-rating"])[1]/strong')


def get_tour_description(driver: WebDriver) -> Optional[str]:
    description_div = driver.find_element(By.ID, "description")
    description = description_div.find_element(By.XPATH, "./p")
    return description.text


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


def get_tour_food_options(driver: WebDriver) -> List[str]:
    """
    Get the food options available for the tour from the webpage.

    If there is more than one option to choose, the button is clickable (enabled)
    and food options are listed in a dropdown list.

    Parameters:
    - driver (WebDriver): The WebDriver object.

    Returns:
    - List[str]: A list of food options available for the tour.
    """
    try:
        food_options_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[2]/div/div/div[3]/div[4]/button"
        button_element = driver.find_element(By.XPATH, food_options_xpath)

        if button_element.is_enabled():  # more than one option available - open dropdown list
            button_element.click()  # open dropdown list
            driver.implicitly_wait(2)

            food_options = get_food_options_from_dropdown_list(driver)

            button_element.click()  # close dropdown list

            return food_options

        else:  # only one option available
            button_text = button_element.text
            food_options = button_text.split("\n")[1:]

        return food_options
    except Exception as e:
        print(f"An error occurred while getting tour food options: {e}")
        return []


def get_food_options_from_dropdown_list(driver: WebDriver):
    """
    Extracts food options from the dropdown list on the Itaka website.

    Parameters:
    - driver: The Selenium WebDriver instance.

    Returns:
    - list: A list of food option names extracted from the dropdown list.
    """
    try:
        # Find all elements within the food options list
        food_opt_elements = driver.find_elements(By.CLASS_NAME, "styles_c__h83a9")
        food_options = []
        # Iterate over each element to extract food option names
        for element in food_opt_elements:
            try:
                food_opt_name = element.text.split("\n")[0]
                food_options.append(food_opt_name)
            except Exception as e:
                print(f"An error occurred while extracting food option name: {e}")
        return food_options
    except Exception as e:
        print(f"An error occurred while getting food options: {e}")
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


def get_departure_options(driver: WebDriver) -> List[str]:
    """
    Get the departure options available for the tour from the webpage.

    If there is more than one option to choose, the button is clickable (enabled)
    and departure options are listed in a dropdown list.

    Parameters:
    - driver (WebDriver): The WebDriver object.

    Returns:
    - List[str]: A list of departure options available for the tour.
    """
    try:
        button_xpath = "/html/body/div[5]/div[4]/div[2]/div/div[1]/div[3]/div[2]/div/div/div[3]/div[5]/button"
        button_element = driver.find_element(By.XPATH, button_xpath)

        if button_element.is_enabled():  # more than one option available - open dropdown list
            button_element.click()  # open dropdown list
            time.sleep(1)

            departure_cities = get_departure_options_from_dropdown_list(driver)

            button_element.click()  # close dropdown list

        else:  # only one option available
            button_value = button_element.text
            departure_cities = button_value.split("\n")[1:]

        return departure_cities
    except Exception as e:
        print(f"An error occurred while getting departure options: {e}")
        return []


def get_departure_options_from_dropdown_list(driver):
    """
    Extracts departure options from the dropdown list.

    Parameters:
    - driver: WebDriver instance

    Returns:
    - List[str]: List of departure cities
    """
    try:
        # Select the dropdown list element
        departure_opt_xpath = "/html/body/div[6]/div/div/div/div[1]"
        departure_opt_element = driver.find_element(By.XPATH, departure_opt_xpath)
        departure_cities = get_default_departure_options(departure_opt_element)
        get_additional_departure_options(departure_cities, departure_opt_element)
        departure_cities = [value.split('\n')[0] for value in departure_cities]  # Extract the city name
        return departure_cities
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_additional_departure_options(departure_cities: List[str], departure_opt_element: WebElement) -> None:
    """
    Extracts additional departure options from the given element and appends them to the list of departure cities.

    Parameters:
    - departure_cities (List[str]): The list of departure cities to which additional options will be appended.
    - departure_opt_element (WebElement): The WebElement containing additional departure options.

    Returns:
    - None
    """
    try:
        additional_list_xpath = "./div/ul/li[@class='styles_c__h83a9']"
        additional_departure_opt_elements = departure_opt_element.find_elements(By.XPATH, additional_list_xpath)
        if additional_departure_opt_elements:  # Check if elements were found
            for element in additional_departure_opt_elements:
                # Extracting the departure information
                label_element = element.find_element(By.CLASS_NAME, "styles_c__label__q3Tzc")
                departure_city = label_element.find_element(By.CLASS_NAME, "oui-font-size-14").text
                departure_cities.append(departure_city)
    except Exception as e:
        print(f"An error occurred: {e}")


def get_default_departure_options(departure_opt_element: WebElement) -> List[str]:
    """
    Extract default departure options from the given element.

    Parameters:
    - departure_opt_element (WebElement): The WebElement containing default departure options.

    Returns:
    - List[str]: A list of default departure cities.
    """
    departure_cities = []
    # Find all li elements within the ul
    li_elements = departure_opt_element.find_elements(By.XPATH, "./ul/li")
    # Iterate over each li element to extract city names
    for li_element in li_elements:
        city_name = li_element.find_element(By.XPATH, ".//span[contains(@class, 'oui-font-size-14')]").text
        departure_cities.append(city_name)

    return departure_cities


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
    tour.rating = get_tour_rating(driver)
    tour.description = get_tour_description(driver)
    tour.country = get_tour_country(driver)
    tour.city = get_tour_city(driver)
    if tour.city is None:
        tour.city = tour.country
    tour.photos = get_tour_photos(driver)
    tour.departure_options = get_departure_options(driver)
    tour.food_options = get_tour_food_options(driver)
    print("tour scrapped successfully\n")
    return tour


if __name__ == "__main__":
    driver = init_webdriver()
    # test_tour_url = "https://www.itaka.pl/wczasy/zjednoczone-emiraty-arabskie/abu-dhabi/hotel-khalidiya-palace-rayhaan-by-rotana,AAEAUH1WKO.html?id=CgVJdGFrYRIEVklUWBoDUExOIgpBQUVBVUgxV0tPKAQ6BEtMMjBCBgiAkeizBkoGCICd%252FbMGUAJiBQoDS1JLagUKA0FVSHIICgZEUDMwMDh6BQoDQVVIggEFCgNLUkuKAQgKBkRQMzAwOJIBBgiAkeizBpoBBgiAnf2zBqIBDAoKUk1TRDAwMDBCMKoBAwoBQQ%253D%253D&participants%5B0%5D%5Badults%5D=2"
    # test_tour_url = "https://www.itaka.pl/wczasy/kenia/twiga-beach-resort-and-spa,MBATWIG.html?id=CgVJdGFrYRIEVklUWBoDUExOIgdNQkFUV0lHKAQ6BEwwNjBCBgiAqqmvBkoGCICfzq8GUAJiBQoDV1JPagUKA01CQXIDCgExegUKA01CQYIBBQoDV1JPigEDCgExkgEGCICqqa8GmgEGCICfzq8GogEFCgNMU1aqAQMKAUE%253D"
    # test_tour_url = "https://www.itaka.pl/wczasy/tunezja/mahdia/hotel-thalassa-mahdia,NBETAMA.html"
    # test_tour_url = "https://www.itaka.pl/wycieczki/slowenia/male-jest-piekne,XSOMALE.html?id=CgVJdGFrYRIEVklUWBoDUExOIgdYU09NQUxFKAY6BEwwNjdCBgiAueywBkoGCIDohrEGUANaCQoHWFNPTUFMRWIFCgNHVUJqBQoDWFNPegUKA1hTT4IBBQoDR1VCkgEGCIDc8bAGmgEGCIDFgbEGogEFCgNEQkyqAQMKAUY%253D&participants%5B0%5D%5Badults%5D=2"
    test_tour_url = "https://www.itaka.pl/wczasy/hiszpania/bilbao/hotel-vincci-consulado-de-bilbao,1015174.html?id=CgVJdGFrYRIEVklURBoDUExOIgcxMDE1MTc0KAM6BEtMMjBCBgiAt%252FivBkoGCICgiLAGUAGSAQYIgLf4rwaaAQYIgKCIsAaiAQUKA0RCTKoBAwoBVQ%253D%253D&participants%5B0%5D%5Badults%5D=2"
    # test_tour_url = "https://www.itaka.pl/wczasy/egipt/marsa-alam/hotel-lazuli,RMFLAZU.html?id=CgVJdGFrYRIEVklUWBoDUExOIgdSTUZMQVpVKAQ6BEwwNjdCBgiA%252FMivBkoGCIDx7a8GUAJiBQoDS1RXagUKA1JNRnIDCgEzegUKA1JNRoIBBQoDS1RXigEDCgEzkgEGCID8yK8GmgEGCIDx7a8GogEFCgNEQkyqAQMKAUE%253D&participants%5B0%5D%5Badults%5D=2"
    test_tour = Tour(test_tour_url)
    test_tour = scrape_single_tour(driver, test_tour)

    # Close the browser
    driver.quit()
