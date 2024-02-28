class Tour:

    name = ""  # tour name
    country = ""  # tour location - country
    city = ""  # tour location - city
    restaurant_details = ""  # restaurant details in the hotel
    food_options = []  # list of strings, available options - 1,2,3 or all-inclusive
    photos = []  # list of strings - links to image hosted online

    def __init__(self, link):
        self.link = link

