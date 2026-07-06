import csv
import sys
from sys import prefix

import requests


PREFIX = "https://api.openf1.org/v1/"
drivers_points: dict[int, int] = {} # driver number, driver points
driver_numbers: dict[str, int] = {} # driver name, driver number

# Sends the API request and turns the returned value into JSON
def request_api(url: str):
    try:
        req = requests.get(url)
        return req.json()
    except requests.exceptions.ConnectionError:
        print("Connection Error, Please check your internet connection")
        sys.exit()


# Sends one request to get the latest results and sorts them into a dictionary for quick lookup later
def get_all_drivers_points():
    req = request_api(f"{PREFIX}championship_drivers?session_key=latest")
    for driver in req:
        drivers_points[driver.get("driver_number")] = driver.get("points_current")
    return

# Gets the points of the given driver from the dictionary
def get_specific_driver_points(number: int) -> int:
    if drivers_points == {}:
        get_all_drivers_points()
    try:
        driver_points = drivers_points[number]
        return driver_points
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


# Reads the RaceNumbers.csv file and puts it into the dictionary
def get_driver_numbers():
    try:
        reader = read_csv("RaceNumbers.csv")
        headers = True
        for row in reader:
            if headers:
                headers = False
                continue
            driver_numbers[row[0]] = int(row[1])
    except FileNotFoundError:
        print("RaceNumbers.csv not found, please get it from the git repo and try again")
        sys.exit()


# Checks if the api is currently locked being a pay wall because a session is live
def check_session_in_progress():
    request = request_api(PREFIX)
    if 'Live F1 session in progress. Global API access (including past sessions) is restricted to authenticated users until the session ends.' in request.get("detail"):
        print("A session is currently in progress, please wait until 30 minutes after the session to run the program again")
        sys.exit()
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    check_session_in_progress()
    get_driver_numbers()
    print(driver_numbers)