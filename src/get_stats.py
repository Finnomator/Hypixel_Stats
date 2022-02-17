import requests
import json


class MojangAPIError(Exception):
    pass


class HypixelAPIError(Exception):
    pass


URL = "https://api.hypixel.net/player?"


def get_data(**kwargs) -> dict:

    complete_url = URL

    for arg in kwargs:
        complete_url += arg + "=" + kwargs[arg] + "&"

    res = requests.get(complete_url).text

    try:
        return json.loads(res)
    except (json.JSONDecodeError, KeyError):
        raise HypixelAPIError("Player not found in hypixel api")


def getuuid(name):
    url = 'https://api.mojang.com/users/profiles/minecraft/'+name
    r = requests.get(url).text
    try:
        return json.loads(r)["id"]
    except (json.JSONDecodeError, KeyError):
        raise MojangAPIError("Player not found in mojang api")


def get_stats(**kwargs) -> dict:

    if not "key" in kwargs:
        raise KeyError("Key must be included")

    if not "name" in kwargs:
        raise KeyError("Playername must be included")

    p_uuid = getuuid(kwargs["name"])
    data = get_data(key=kwargs["key"], uuid=p_uuid)

    return data
