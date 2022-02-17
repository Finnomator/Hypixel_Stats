from datetime import datetime
import json
import sys
from threading import Thread
import os
from tqdm import tqdm
import detect_who
import mc_setup
import process.process_data as process_data
import time

players_to_search = []

mc_setup.main()

with open("info.json", "r") as f:
    infos = json.load(f)

api_key = infos["api_key"]
mc_version = infos["mc_version"]
mc_client = infos["client"]


detector = detect_who.main(mc_client, mc_version)


def log_exception(exception: str):

    with open("log.json", "r") as f:
        log_data = json.load(f)

    log_data.update({str(datetime.now()): str(exception)})

    with open("log.json", "w") as f:
        json.dump(log_data, f, indent=4)


def update_infos(data: dict):

    with open("info.json", "r") as f:
        old = json.load(f)

    old.update(data)

    with open("info.json", "w") as f:
        json.dump(old, f, indent=4)

    return old


def reset_left_requests(stop):

    while not stop():
        min_now = datetime.now().minute

        if min_now != infos["request"]["last_request"]:
            update_infos(
                {"request": {"left_requests": 120, "last_request": min_now}})

        time.sleep(5)


stop_thread = False
t1 = Thread(target=reset_left_requests, args=(lambda: stop_thread, ))
t1.start()


while True:

    print("Ready, use /who in game")

    try:
        for detect in detector:

            os.system("cls")

            print("Searching...")

            players_data = {}

            left_requests = infos["request"]["left_requests"]

            for player in tqdm(detect):

                if left_requests == 0:
                    print("Out of requests, please wait 60s")
                    break

                processed_player_data = process_data.process_player_data(
                    player, key=api_key, name=player)
                players_data.update({player: processed_player_data})

                left_requests -= 1

            extracted_player_data = process_data.extract(players_data)

            pretty_res = process_data.pretty_format(extracted_player_data)

            infos = update_infos(
                {"request": {"left_requests": left_requests, "last_request": datetime.now().minute}})

            print(pretty_res)

        time.sleep(0.1)

    except KeyboardInterrupt:
        print("Stopping...")
        stop_thread = True
        t1.join()
        exit()

    except Exception as e:

        e_msg = ""
        unwichtig, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        e_msg += str(fname)
        e_msg += " (l."+str(exc_tb.tb_lineno)+"): "
        e_msg += str(e)

        print("An exception occurred: " + str(e))
        print("See src/log.json for more information")
        print("If this error occurres again please report it on https://github.com/Finnomator/Hypixel_Stats/issues")
        log_exception(e_msg)
