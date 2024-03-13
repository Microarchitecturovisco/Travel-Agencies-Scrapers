import pathlib
from typing import List

import pandas as pd

from logic.initalize_scraper import init_webdriver
from logic.tours.scrapping_tours_urls import scrape_all_inclusive_tours
from logic.tours.scrapping_single_tour import scrape_single_tour
from logic.tours.tour_class import Tour


def save_dataframe(tours: List[Tour]):

    pathlib.Path('./data').mkdir(parents=True, exist_ok=True)

    for i, tr in enumerate(tours):
        tr.id = i

    pd.DataFrame(
        [[tr.id, photo] for tr in tours for photo in tr.photos],
        columns=['idHotel', 'photoUrl']
    ).to_csv(pathlib.Path('./data/hotel_photos.csv'), sep='\t', index=False)

    pd.DataFrame(
        [[tr.id, food_option] for tr in tours for food_option in tr.food_options],
        columns=['idHotel', 'foodOption']
    ).to_csv(pathlib.Path('./data/hotel_food_options.csv'), sep='\t', index=False)

    pd.DataFrame(
        [[tr.id, departure_option] for tr in tours for departure_option in tr.departure_options],
        columns=['idHotel', 'departureOption']
    ).to_csv(pathlib.Path('./data/hotel_departure_options.csv'), sep='\t', index=False)

    pd.DataFrame(
        [[tr.id, room.name, room.description, room.price] for tr in tours for room in tr.rooms],
        columns=['idHotel', 'name', 'description', 'price']
    ).to_csv(pathlib.Path('./data/hotel_rooms.csv'), sep='\t', index=False)

    pd.DataFrame(
        [[tr.id, tr.name, tr.description, tr.rating, tr.country, tr.city, tr.restaurant_details, ] for tr in tours],
        columns=['id', 'name', 'description', 'rating', 'country', 'city', 'restaurantDetails']
    ).to_csv(pathlib.Path('./data/hotels.csv'), sep='\t', index=False)


if __name__ == "__main__":
    driver = init_webdriver()

    tours_result = [scrape_single_tour(driver, tour) for tour in scrape_all_inclusive_tours(driver)]

    save_dataframe(tours_result)

    # Close the browser
    driver.quit()
