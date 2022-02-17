from datetime import datetime
import json
import sys
import os
from tqdm import tqdm
import detect_who
import mc_setup
import process.process_data as process_data
import time

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

    global infos

    infos.update(data)

    with open("info.json", "w") as f:
        json.dump(infos, f, indent=4)


def reset_left_requests():

    min_now = datetime.now().minute

    if min_now != infos["request"]["last_request"]:
        update_infos(
            {"request": {"left_requests": 120, "last_request": min_now}})

print()
print("#"*51)
print("# Please make sure you only have one instance of  #\n# this program runnig or else you will waste your #\n# api requests (which are limited to 120/min)     #")
print("#"*51)
print()

reset_left_requests()

while True:

    print("Ready, use /who in game")

    try:
        for detect in detector:

            os.system("cls")

            print("Searching...")

            players_data = {}

            reset_left_requests()

            left_requests = infos["request"]["left_requests"]

            for player in tqdm(detect):

                if left_requests == 0:
                    break

                processed_player_data = process_data.process_player_data(
                    player, key=api_key, name=player)
                players_data.update({player: processed_player_data})

                left_requests -= 1

            update_infos(
                {"request": {"left_requests": left_requests, "last_request": datetime.now().minute}})

            if left_requests == 0:
                print("Out of requests, please wait 60s")
                continue

            extracted_player_data = process_data.extract(players_data)

            pretty_res = process_data.pretty_format(extracted_player_data)

            print(pretty_res)

        time.sleep(0.1)

    except KeyboardInterrupt:
        print("Stopping...")
        exit()

    except Exception as e:

        e_msg = ""
        _, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        e_msg += str(fname)
        e_msg += " (l."+str(exc_tb.tb_lineno)+"): "
        e_msg += str(e)

        print("An exception occurred: " + str(e))
        print("Check src/log.json for more information")
        print("If this error occurres again please report it on https://github.com/Finnomator/Hypixel_Stats/issues")
        log_exception(e_msg)
