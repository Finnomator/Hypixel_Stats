import get_stats
import process.filter_data as filter_data
import process.extract_for_mode as extract_for_mode
import json


def process_player_data(player, **kwargs):

    filtered = {}

    with open("process/filters.json", "r") as f:
        data_filter = json.load(f)

    try:
        data = get_stats.get_stats(**kwargs)
        filtered = filter_data.main(data, data_filter, False)

    except get_stats.MojangAPIError:
        filtered = "Not found in Mojang API"

    except get_stats.HypixelAPIError:
        filtered = "Not found in Hypixel API"

    return filtered


def extract(data: dict):
    res_data = extract_for_mode.extract(data)
    return res_data


def pretty_format(data: dict):

    data_formatted = json.dumps(data, indent=4)

    res = data_formatted.replace("{", "").replace("}", "").replace(
        '"', "").replace(",", "").replace("\n    ", "\n").replace("    ", " | ")

    return res
