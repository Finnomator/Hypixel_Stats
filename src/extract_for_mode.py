def get_mode(player_data: dict):

    for key in player_data:

        if "mostRecentGameType" in player_data[key] and player_data[key] != None:

            return player_data[key]["mostRecentGameType"]

    return None


def extract(data: dict):

    extracted_data = data.copy()

    for i, p in enumerate(data):
        player_data = data[list(data.keys())[i]]

        if isinstance(player_data, dict):
            break

        if i == len(list(data.keys()))-1:
            return data

    mode = get_mode(player_data)

    if mode == None:
        return data

    for player_name in data:
        try:
            for mode_in_data in data[player_name]["stats"]:

                if mode_in_data.lower().replace("_", "") == mode.lower().replace("_", ""):

                    if "Overall" in data[player_name]:
                        extracted_data.update(
                            {player_name: {"Overall": data[player_name]["Overall"], mode_in_data: data[player_name]["stats"][mode_in_data]}})

                    else:
                        extracted_data.update(
                            {player_name: {mode_in_data: data[player_name]["stats"][mode_in_data]}})
                    break

        except TypeError:
            extracted_data[player_name] = data[player_name]

    return extracted_data
