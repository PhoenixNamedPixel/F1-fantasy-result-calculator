import sys
import requests


PREFIX = "https://api.openf1.org/v1/"


# Sends the API request and turns the returned value into JSON
def request_api(url: str):
    try:
        req = requests.get(url)
        return req.json()
    except requests.exceptions.ConnectionError:
        print("Connection Error, Please check your internet connection")
        sys.exit()


# Gets the points of the given driver
def get_specific_driver_points(number: int) -> int:
    try:
        req = request_api(f"{PREFIX}championship_drivers?session_key=latest&&driver_number={number}")
        return req[0].get("points_current")
    except KeyError:
        print("Not a valid driver number")
        sys.exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(get_specific_driver_points(9))