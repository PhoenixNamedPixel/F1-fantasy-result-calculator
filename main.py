import csv
import sys
from sys import prefix

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
        print(f"{number} is not a valid driver number")
        sys.exit()


# Read the given csv file and return it line by line as needed
def read_csv(filename: str):
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row


# Reads Teams.csv and puts it into a dictionary
def get_teams():
    try:
        reader = read_csv("Teams.csv")
        teams = {}
        headers = True
        for row in reader:
            if headers:
                headers = False
                continue
            teams[row[0]] = row[1:]
        if teams == {}:
            print("Please fill in the teams within Teams.csv and run the program again")
            sys.exit()
        return teams
    except FileNotFoundError:
        print("Teams.csv not found, please create and fill it first and try again")
        sys.exit()


def get_driver_numbers() -> dict[str, int]:
    try:
        reader = read_csv("RaceNumbers.csv")
        driver_numbers = {}
        headers = True
        for row in reader:
            if headers:
                headers = False
                continue
            driver_numbers[row[0]] = row[1]
        return driver_numbers
    except FileNotFoundError:
        print("RaceNumbers.csv not found, please get it from the git repo and try again")
        sys.exit()


def get_driver_points():
    driver_points = {}
    driver_numbers = get_driver_numbers()
    for driver in driver_numbers:
        driver_points[driver] = get_specific_driver_points(driver_numbers[driver])
    return driver_points


def check_session_in_progress():
    request = request_api(PREFIX)
    if 'Live F1 session in progress. Global API access (including past sessions) is restricted to authenticated users until the session ends.' in request.get("detail"):
        print("A session is currently in progress, please wait until 30 minutes after the session to run the program again")
        sys.exit()
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    check_session_in_progress()
    print(get_driver_points())