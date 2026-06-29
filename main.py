import requests


PREFIX = "https://api.openf1.org/v1/"


# Sends the API request and turns the returned value into JSON
def request_api(url: str):
    req = requests.get(url)
    return req.json()


# Gets the points of the given driver
def get_specific_driver_points(number: int) -> int:
    req = request_api(f"{PREFIX}championship_drivers?session_key=latest&&driver_number={number}")
    return req[0].get("points_current")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(get_specific_driver_points(12))