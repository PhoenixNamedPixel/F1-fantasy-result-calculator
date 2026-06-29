import requests


PREFIX = "https://api.openf1.org/v1/"


## Sends the API request and turns the returned value into JSON
def request_api(url: str) -> requests.Response:
    req = requests.get(url)
    return req.json()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(request_api(PREFIX + "championship_drivers?session_key=latest"))