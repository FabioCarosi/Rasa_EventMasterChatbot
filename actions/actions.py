from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests


api_key = "<API-KEY-TicketMaster>"


class EventSearch(Action):
    def name(self) -> Text:
        return "action_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Get the entities recognized in the latest user message
        entities = tracker.latest_message["entities"]
        # Send a message to the user saying "YOUR RESEARCH:"
        dispatcher.utter_message(text="YOUR RESEARCH: ")
        msg = ""
        # Iterate through the entities and send a message to the user
        # with the entity value, type, and role (if available)
        for entity in entities:
            msg = "KEYWORD: " + entity["value"] + " TYPE: " + entity["entity"]
            if entity.get("role"):
                msg = msg + " ROLE: " + entity["role"]
            dispatcher.utter_message(text=msg)

        # Call the search function with the entities as the argument
        string_array = search(entities)
        count = 0
        max = 5
        # Iterate through the results returned by the search function
        # and send a message to the user with each result
        # Up to a maximum of 5 results
        for string in string_array:
            dispatcher.utter_message(text=string)

            count = count + 1
            if count == max:
                break
        return []


class GetEventDetails(Action):
    def name(self) -> Text:
        return "action_detail"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Get the entities recognized in the latest user message
        entities = tracker.latest_message["entities"]
        msg = ""
        # Iterate through the entities and send a message to the user
        # with the event id
        for entity in entities:
            msg = "Event ID: " + entity["value"]
            dispatcher.utter_message(text=msg)

        # Call the detail function with the entities as the argument
        string_array = detail(entities)
        count = 0
        max = 5
        # Iterate through the results returned by the detail function
        # and send a message to the user with each result
        # Up to a maximum of 5 results
        for string in string_array:
            dispatcher.utter_message(text=string)

            count = count + 1
            if count == max:
                break
        return []


country_codes = {
    "united states of america": "US",
    "united states": "US",
    "usa": "US",
    "andorra": "AD",
    "anguilla": "AI",
    "argentina": "AR",
    "australia": "AU",
    "austria": "AT",
    "azerbaijan": "AZ",
    "bahamas": "BS",
    "bahrain": "BH",
    "barbados": "BB",
    "belgium": "BE",
    "bermuda": "BM",
    "brazil": "BR",
    "bulgaria": "BG",
    "canada": "CA",
    "chile": "CL",
    "china": "CN",
    "colombia": "CO",
    "costa rica": "CR",
    "croatia": "HR",
    "cyprus": "CY",
    "czech republic": "CZ",
    "denmark": "DK",
    "dominican republic": "DO",
    "ecuador": "EC",
    "estonia": "EE",
    "faroe islands": "FO",
    "finland": "FI",
    "france": "FR",
    "georgia": "GE",
    "germany": "DE",
    "ghana": "GH",
    "gibraltar": "GI",
    "great Britain": "GB",
    "greece": "GR",
    "hong kong": "HK",
    "hungary": "HU",
    "iceland": "IS",
    "india": "IN",
    "ireland": "IE",
    "israel": "IL",
    "italy": "IT",
    "italia": "IT",
    "jamaica": "JM",
    "japan": "JP",
    "korea, republic of": "KR",
    "korea": "KR",
    "republic of korea": "KR",
    "south korea": "KR",
    "latvia": "LV",
    "lebanon": "LB",
    "lithuania": "LT",
    "luxembourg": "LU",
    "malaysia": "MY",
    "malta": "MT",
    "mexico": "MX",
    "monaco": "MC",
    "montenegro": "ME",
    "morocco": "MA",
    "netherlands": "NL",
    "netherlands antilles": "AN",
    "new zealand": "NZ",
    "northern ireland": "ND",
    "norway": "NO",
    "peru": "PE",
    "poland": "PL",
    "portugal": "PT",
    "romania": "RO",
    "russian federation": "RU",
    "saint lucia": "LC",
    "saudi arabia": "SA",
    "serbia": "RS",
    "singapore": "SG",
    "slovakia": "SK",
    "south africa": "ZA",
    "spain": "ES",
    "sweden": "SE",
    "switzerland": "CH",
    "taiwan": "TW",
    "thailand": "TH",
    "trinidad and tobago": "TT",
    "turkey": "TR",
    "ukraine": "UA",
    "united arab emirates": "AE",
    "uae": "AE",
    "uruguay": "UY",
    "venezuela": "VE",
}

segment_codes = {
    "arts & theater": "KZFzniwnSyZfZ7v7na",
    "art": "KZFzniwnSyZfZ7v7na",
    "arts": "KZFzniwnSyZfZ7v7na",
    "theater": "KZFzniwnSyZfZ7v7na",
    "miscellaneous": "KZFzniwnSyZfZ7v7n1",
    "miscellany": "KZFzniwnSyZfZ7v7n1",
    "music": "KZFzniwnSyZfZ7v7nJ",
    "musics": "KZFzniwnSyZfZ7v7nJ",
    "sports": "KZFzniwnSyZfZ7v7nE",
    "sport": "KZFzniwnSyZfZ7v7nE",
}


def getCountryCode(country_name):
    """
    This function receives a country name and returns its corresponding
    country code using a dictionary that maps country names to codes.
    If the input country name is already in the format of a country code,
    it is returned as is. If the input country name is not found in the
    dictionary, the function returns an error message.
    """
    codes = country_codes.values()
    # Check if the input is already a valid country code
    if country_name in codes:
        return country_name
    else:
        # Convert input to string and lowercase it
        country_name = str(country_name)
        country_name = country_name.lower()
        # Lookup the country name in the dictionary
        code = country_codes.get(country_name)
        if code:
            return code
        else:
            return "ERRORCODE_01: Country not found"


def getSegmentId(segment_name):
    """
    This function receives a segment name and returns its corresponding
    segment id using a dictionary that maps segment names to ids.
    If the input segment name is already in the format of a segment id,
    it is returned as is. If the input segment name is not found in the
    dictionary, the function returns an error message.
    """
    codes = segment_codes.values()
    # Check if the input is already a valid segment id
    if segment_name in codes:
        return segment_name
    else:
        # Convert input to string and lowercase it
        segment_name = str(segment_name)
        segment_name = segment_name.lower()
        # Lookup the segment name in the dictionary
        id = segment_codes.get(segment_name)
        if id:
            return id
        else:
            return "ERRORCODE_02: Segment not found"


def search(entities):
    """
    This function receives a list of entities extracted from the user input by the NLU model and constructs a
    Ticketmaster Discovery API url to search for events based on the entities.
    The function handles different entities such as city, country, artist, segment and date range.
    It returns an array of strings containing the event details such as name, venue, date and time, event id and url.
    """
    # Base url for the Ticketmaster Discovery API
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&locale=*"

    string_array = []
    city = ""
    country = ""
    artist = ""
    segment = ""
    start_date = ""
    end_date = ""
    # Iterate through the entities and construct the url with the appropriate parameters
    for entity in entities:
        if entity["entity"] == "city":
            city = "&city=" + entity["value"]
        if entity["entity"] == "country":
            # Get the country code using the getCountryCode function
            country = "&countryCode=" + getCountryCode(entity["value"])
        if entity["entity"] == "artist":
            artist = "&keyword=" + entity["value"]
        if entity["entity"] == "segment":
            # Get the segment id using the getSegmentId function
            segment = "&segmentId=" + getSegmentId(entity["value"])
        if entity["entity"] == "date":
            string_array.append("PLEASE NOTE: DATES MUST BE IN YYYY-MM-DD FORMAT")
            if entity["role"] == "start":
                start_date = "&startDateTime=" + entity["value"] + "T00:00:00Z"
            if entity["role"] == "end":
                end_date = "&endDateTime=" + entity["value"] + "T00:00:00Z"

    # Append the parameters to the base url
    url = url + city + country + artist + segment + start_date + end_date

    if "ERRORCODE_" in url:
        # Return error message if any of the keywords is not supported by the API
        string_array.append("Error in keywords")
        string_array.append(
            "One or more of the keywords entered is not supported by the API"
        )
        return string_array

    # Send the request to the API and get the response
    response = requests.get(url)
    # Print the url for debugging purposes
    print(url)

    if response.status_code == 200:
        # If the response is OK, parse the JSON data
        data = response.json()
        embedded = data.get("_embedded")
        if embedded:
            events = embedded.get("events")
            if events:
                for event in data["_embedded"]["events"]:
                    # Create a string with the event details
                    string = (
                        event["name"]
                        + "\n"
                        + event["_embedded"]["venues"][0]["name"]
                        + " "
                        + event["dates"]["start"]["localDate"]
                        + " - "
                        + event["dates"]["start"]["localTime"]
                        + "\n"
                        + "EventId: "
                        + event["id"]
                        + "\n"
                        + event["url"]
                    )
                    # Append the string to the string_array
                    string_array.append(string)
            else:
                string_array.append("NO EVENTS FOUND")
        else:
            string_array.append("NO EVENTS FOUND. SORRY :(")

    else:
        string_array.append("BAD REQUEST")
    return string_array


def detail(entities):
    # initialize event_id variable with error code
    event_id = "ERRORCODE_03"

    # loop through entities to find the event_id value
    for entity in entities:
        if entity["entity"] == "event_id":
            event_id = entity["value"]

    # construct the url for the API request
    url = (
        "https://app.ticketmaster.com/discovery/v2/events/"
        + event_id
        + "?apikey="
        + api_key
        + "&locale=*"
    )
    # initialize an empty list for the string array
    string_array = []
    # if event_id is not found, return an error message
    if event_id == "ERRORCODE_03":
        string_array.append("Error in event_id")
        string_array.append(
            "One or more of the keywords entered is not supported by the API"
        )
        string_array.append(event_id)
        return string_array
    response = requests.get(url)
    print(url)

    # Check the status code of the response
    # If the status code is 200, it means the request was successful
    if response.status_code == 200:
        data = response.json()
        # Get the event name and URL
        if data.get("name"):
            string_array.append(data["name"] + "\n" + data["url"])

        # Get the dates
        start = data["dates"]["start"]
        if start:
            string_array.append(
                "Event date: "
                + data["dates"]["start"]["localTime"]
                + " "
                + data["dates"]["start"]["localDate"]
            )
        # Get the info and seatmap
        if data.get("info"):
            string_array.append("Info:\n" + data["info"])
        if data.get("seatmap"):
            string_array.append("Seatmap: " + data["seatmap"]["staticUrl"])

        # Get the public sales e exclusive presales with prices
        sales = data.get("sales")
        if sales.get("public"):
            string_array.append(
                "Start public sale: "
                + data["sales"]["public"]["startDateTime"]
                + "\n"
                + "End public sale: "
                + data["sales"]["public"]["endDateTime"]
            )
        presales = sales.get("presales")
        if presales:
            for presale in presales:
                name = ""
                description = ""
                if presale.get("name"):
                    name = "\n" + presale["name"]
                if presale.get("description"):
                    description = "\n" + presale["description"]
                string_array.append(
                    name
                    + description
                    + "Start presale sale: "
                    + presale["startDateTime"]
                    + "\n"
                    + "End public sale: "
                    + presale["endDateTime"]
                )
        if data.get("priceRanges"):
            string_array.append(
                "Price range: "
                + str(data["priceRanges"][0]["min"])
                + " - "
                + str(data["priceRanges"][0]["max"])
                + " "
                + data["priceRanges"][0]["currency"]
            )

        # Get venue infos
        venues = data.get("_embedded").get("venues")
        if venues:
            venue = data["_embedded"]["venues"][0]
            if venue.get("address"):
                string_array.append(
                    venue["name"]
                    + "\n"
                    + venue["address"]["line1"]
                    + "\n"
                    + venue["city"]["name"]
                    + ", "
                    + venue["country"]["name"]
                )
            else:
                string_array.append(
                    venue["name"]
                    + "\n"
                    + venue["city"]["name"]
                    + ", "
                    + venue["country"]["name"]
                )

    else:
        string_array.append("BAD REQUEST")
    return string_array
