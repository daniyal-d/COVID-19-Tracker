import json
from datetime import time
import requests

key = "t37zQwBDTofT"  # API key
p_token = "tipxNh4q9VpT"  # API token

info = input("Coronavirus Tracker \n \n What do you wish to view \n \n Type 'wc' for worldwide cases \n Type 'wd' for worldwide deaths \n Type 'wr' for worldwide recoveries \n Type 'c' for the info on a specific country \n")


class Tracker:
    def __init__(self, key, p_token):
        self.key = key
        self.p_token = p_token
        self.params = {
            "key": self.key
        }
        self.stats = self.data()

    def data(self):
        case = requests.get(f"https://www.parsehub.com/api/v2/projects/{p_token}/last_ready_run/data", params={"api_key": key}) # Use web scraping to find data
        stats = json.loads(case.text) # Use the JSON format of the data
        return stats

    def worldwide_cases(self):
        world = self.stats["world_total"] # Find total worldwide cases
        for data in world:
            if data["name"] == "Coronavirus Cases:":
                return data["world_cases"]

    def worldwide_deaths(self):
        world = self.stats["world_total"] # Find total worldwide deaths
        for data in world:
            if data["name"] == "Deaths:":
                return data["world_cases"]

    def worldwide_recovered(self):
        world = self.stats["world_total"] # Find total worldwide recoveries
        for data in world:
            if data["name"] == "Recovered:":
                return data["world_cases"]

    def states(self):
        country = self.stats["states"] # Find info for a specific country
        state = input("Which countries data do you want to view?: ") # Ask which countries data a user wishes to view
        for data in country:
            if data["name"].lower() == state.lower():
                return (f"Info for {state} \n Cases: {data['states_cases']} \n Deaths: {data['states_deaths']} \n Recoveries: {data['states_recovered']}")

    def new_info(self, threading=None):
        hello = requests.post(f'https://www.parsehub.com/api/v2/projects/{p_token}/run', params={"api_key": key}) # Updates data
        stats = json.loads(hello.text) # JSON form of updated data

        def update():
            time.sleep(0.1)
            old_info = self.stats
            while True:
                new_info = stats()
                if new_info != old_info:
                    self.stats = new_info # Convert old data into new data
                    break
                time.sleep(0.1)
        data.new_info()
        threading = threading.Thread(target=update)
        threading.start()


data = Tracker(key, p_token)
if info == "wc":
    print(f"Worldwide Cases: {data.worldwide_cases()}")

elif info == "wd":
    print(f"Worldwide Deaths: {data.worldwide_deaths()}")

elif info == "wr":
    print(f"Worldwide Recoveries: {data.worldwide_recovered()}")

elif info == "c":
    print(data.states())
