import pathlib
from typing import Dict, List, AnyStr

from tqdm.auto import tqdm
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd

from initalize_scraper import init_webdriver


def scrape_destinations() -> Dict[AnyStr, List[AnyStr]]:
    """
    Scrapes destinations from the 'Where do you want to go?' button on the main page

    Returns
    -------
    Dict[AnyStr, List[AnyStr]]
        A dict where country strings are keys and values are lists of available regions in that country
    """
    driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[1]/div[2]/div[2]/div/div/div[1]/div/label').click()

    destinations_list_items = (driver.find_element(By.CLASS_NAME, 'styles_c__inner__gsYGX')
                               .find_element(By.CLASS_NAME, 'col-md')
                               .find_elements(By.TAG_NAME, 'li'))

    ret_destinations = {}

    for destination in tqdm(destinations_list_items):
        country_name = destination.find_element(By.CLASS_NAME, 'styles_c__label__sqHYM').text

        ret_destinations[country_name] = []

        try:
            expand_regions_button = destination.find_element(By.CLASS_NAME, 'ms-2').find_element(By.TAG_NAME, 'button')

            expand_regions_button.click()

            regions = destination.find_elements(By.CLASS_NAME, 'styles_c__label__sqHYM')[1:]

            for region in regions:
                ret_destinations[country_name].append(region.text)
        except NoSuchElementException:
            pass

    return ret_destinations


def save_dataframe(destinations: Dict[AnyStr, List[AnyStr]]) -> None:
    """
    Responsible for creating a Pandas dataframe from the scraped destinations and exporting it to a CSV file

    Parameters
    ----------
    destinations: Dict[AnyStr, List[AnyStr]]
        dictionary with countries along with their regions as lists
    """
    flattened_destinations = []
    for country, regions_list in destinations.items():
        if not len(regions_list):
            flattened_destinations.append([country, ''])
            continue

        for region in regions_list:
            flattened_destinations.append([country, region])

    dataframe = pd.DataFrame(flattened_destinations, columns=["Country", "Region"])

    print(f'\n{dataframe}')

    pathlib.Path('./data').mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(pathlib.Path('./data/destinations.csv'), sep='\t')


if __name__ == "__main__":
    driver = init_webdriver()

    save_dataframe(scrape_destinations())

    driver.quit()
