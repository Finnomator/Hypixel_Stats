from datetime import datetime
import json
from threading import Thread
from os import system
from tqdm import tqdm
import get_stats
import detect_who
import setup
import filter_data
import time

players_to_search = []

setup.main()

with open("info.json", "r") as f:
    infos = json.load(f)

api_key = infos["api_key"]
mc_version = infos["mc_version"]
mc_client = infos["client"]


detector = detect_who.main(mc_client, mc_version)


def update_infos(data: dict):

    with open("info.json", "r") as f:
        old = json.load(f)

    old.update(data)

    with open("info.json", "w") as f:
        json.dump(old, f, indent=4)

    return old


def reset_left_requests(stop):

    while not stop:
        min_now = datetime.now().minute

        if min_now != infos["request"]["last_request"]:
            update_infos(
                {"request": {"left_requests": 120, "last_request": min_now}})

        time.sleep(1)


stop_thread = False
t1 = Thread(target=reset_left_requests, args=(lambda: stop_thread, ))
t1.start()

with open("filters.json", "r") as f:
    data_filter = json.load(f)

print("Ready, use /who in game")

while True:
    try:
        for detect in detector:

            system("cls")

            print("Searching...")

            filtered_obj = {}

            left_requests = infos["request"]["left_requests"]

            players_to_search = detect

            for player in tqdm(players_to_search):

                if left_requests == 0:
                    print("Out of requests, please wait 60 secs")
                    break

                try:
                    data = get_stats.get_stats(key=api_key, name=player)
                    filtered = filter_data.main(data, data_filter, True)
                    filtered_obj.update({player: filtered})

                except get_stats.MojangAPIError:
                    filtered_obj.update({player: "Not found in Mojang API"})

                except get_stats.HypixelAPIError:
                    filtered_obj.update({player: "Not found in Hypixel API"})

                left_requests -= 1

            print(json.dumps(filtered_obj, indent=4))

            infos = update_infos(
                {"request": {"left_requests": left_requests, "last_request": datetime.now().minute}})

            print("\nUse /who to refresh")

        time.sleep(0.1)
    except KeyboardInterrupt:
        stop_thread = True
        t1.join()
        exit()
