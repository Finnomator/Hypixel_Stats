import json
import os
import requests
from pathlib import Path

URL = "https://api.hypixel.net/player?"


SUPPORTED_CLIENTS = ["default", "lunar"]
valid_versions = []

home = str(Path.home()) + "/"

with open("info.json","r") as f:
    infos = json.load(f)


def get_vaild_versions():

    global valid_versions

    if infos["client"] == "default":
        return "default"

    if infos["client"] == "lunar":
        valid_versions = os.listdir(home + ".lunarclient/offline")

    return valid_versions


def update_infos(data: dict):

    with open("info.json","r") as f:
        old = json.load(f)

    old.update(data)

    with open("info.json","w") as f:
        json.dump(old, f, indent=4)

    return old


def is_valid_key(key):
    resp = requests.get(URL + "key="+key).text
    if json.loads(resp)["cause"] == "Invalid API key":
        return False
    return True


def is_valid_client(client):

    if client in SUPPORTED_CLIENTS:
        return True

    return False

def is_valid_version(version):

    if infos["client"] == "default":
        return True

    if infos["mc_version"] in valid_versions:
        return True

    if version in valid_versions:
        return True

    return False


def get_api_key():

    if is_valid_key(infos["api_key"]):
        return infos

    print("You can optain your api key by using the command '/key' on the hypixel server")
    
    while True:
        entered_key = input("Enter key: ")
        if is_valid_key(entered_key):
            break
        print("Invalid key")

    return update_infos({"api_key": entered_key})


def get_launcher():

    if is_valid_client(infos["client"]):
        return infos

    print("Enter the launcher you are using (", end = "")
    for i, l in enumerate(SUPPORTED_CLIENTS):
        ennd = ")\n" if i == len(SUPPORTED_CLIENTS)-1 else "|"
        print(l, end = ennd)
    
    while True:
        entered_launcher = input("Enter launcher: ")
        if is_valid_client(entered_launcher):
            break
        print("Invalid launcher")

    return update_infos({"client": entered_launcher})


def get_version():

    if is_valid_version(infos["mc_version"]):
        return infos

    if len(valid_versions) == 1:
        return update_infos({"mc_version": valid_versions[0]})

    print("Enter the version you are using (", end = "")
    for i, l in enumerate(valid_versions):
        ennd = ")\n" if i == len(valid_versions)-1 else "|"
        print(l, end = ennd)
    
    while True:
        entered_version = input("Enter version: ")
        if is_valid_version(entered_version):
            break
        print("Invalid version")

    return update_infos({"mc_version": entered_version})


def main():

    global infos

    infos = get_api_key()
    infos = get_launcher()

    get_vaild_versions()

    infos = get_version()


if __name__ == "__main__":
    main()