def get_mode(player_data: dict):

    for key in player_data:

        if "mostRecentGameType" in player_data[key]:

            return player_data[key]["mostRecentGameType"]

    return None


def extract(data: dict):

    extracted_data = data.copy()

    player_data = data[list(data.keys())[0]]

    mode = get_mode(player_data)

    if mode == None:
        return data        

    for player_name in data:
        for mode_in_data in data[player_name]["stats"]:

            if mode_in_data.lower() == mode.lower():

                extracted_data[player_name] = data[player_name]["stats"][mode_in_data]

    return extracted_data
