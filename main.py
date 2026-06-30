import csv
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
        return teams
    except FileNotFoundError:
        print("Teams.csv not found, please create it first and try again")
        sys.exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(get_teams())