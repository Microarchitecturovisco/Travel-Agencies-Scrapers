class Tour:
    """
    Represents a tour with various details.

    Attributes:
    - name (str): The name of the tour.
    - country (str): The country where the tour takes place.
    - city (str): The city where the tour takes place.
    - restaurant_details (str): Details about the restaurant in the hotel.
    - food_options (List[str]): Available food options for the tour.
    - photos (List[str]): URLs of photos related to the tour.
    - airport_options (List[str]): Available airport options for the tour.
    - url (str): The url to the tour webpage (the original Itaka website).
    """

    name = ""
    rating = ""
    description = ""
    country = ""
    city = ""
    restaurant_details = ""
    food_options = []
    photos = []
    airport_options = []
    rooms = []

    def __init__(self, url: str):
        """
        Initialize a Tour object with the given url.

        Parameters:
        - url (str): The url to the tour webpage.
        """
        self.url = url
