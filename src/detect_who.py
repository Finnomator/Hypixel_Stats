from io import TextIOWrapper
from pathlib import Path
import time


def get_log(client, mc_version):

    home = str(Path.home()) + "/"

    if client == "lunar":
        log_path = home + ".lunarclient/offline/" + mc_version + "/logs/latest.log"

    else:
        log_path = home + "AppData/Roaming/.minecraft/logs/latest.log"

    if not Path.exists(Path(log_path)):
        raise FileNotFoundError("Failed to locate log file " + log_path)

    with open(log_path, "r") as f:
        log_text = f.read()

    return log_text, log_path


def follow(thefile: TextIOWrapper):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line.replace("\n","")


def extract(line: str, file: TextIOWrapper):

    players = []
    found = True

    if "[Client thread/INFO]: [CHAT] ONLINE: " in line:
        msg = line.split("ONLINE: ")[1]
        players = msg.split(", ")
        
    elif "[Client thread/INFO]: [CHAT] Team #1 - " in line:
        time.sleep(0.3)
        file.seek(0)

        file_data = file.readlines()[::-1]
        temp = []
        for l in file_data:
            temp.append(l.replace("\n",""))
        file_data = temp.copy()

        end_offset = 0

        while not "[Client thread/INFO]: [CHAT] Team #1" in file_data[end_offset]:
            end_offset += 1
        
        team_c = 0
        teams = []

        team_line = file_data[end_offset]

        while "[Client thread/INFO]: [CHAT] Team #" in team_line:
            team_c += 1

            team = team_line.split(" - [")[1].split("]")[0]

            if ", " in team:
                team = team.split(", ")

                for t in team:
                    teams.append(t)

            else:
                teams.append(team)

            team_line = file_data[end_offset - team_c]

        players = teams.copy()
        

    elif "[Client thread/INFO]: [CHAT] Team #1: " in line:
        time.sleep(0.3)
        file.seek(0)

        file_data = file.readlines()[::-1]
        temp = []
        for l in file_data:
            temp.append(l.replace("\n",""))
        file_data = temp.copy()

        end_offset = 0

        while not "[Client thread/INFO]: [CHAT] Team #1: " in file_data[end_offset]:
            end_offset += 1
        
        team_c = 0
        teams = []

        team_line = file_data[end_offset]

        while "[Client thread/INFO]: [CHAT] Team #" in team_line:
            team_c += 1

            team = team_line.split("[CHAT] Team #"+str(team_c)+": ")[1]

            if ", " in team:
                team = team.split(", ")

                for t in team:
                    teams.append(t)

            else:
                teams.append(team)

            team_line = file_data[end_offset - team_c]

        players = teams.copy()


    else:
        found = False

    if found:
        if " [x" in players[len(players)-1]:
            players[len(players)-1] = players[len(players)-1].split(" [x")[0]

    return found, players


def main(client = "default", mc_version = ""):

    """
    Available clients:
    - default
    - lunar

    mc_version must be give if the client is not "default" as string (e.g. "1.8" or "1.16")
    """

    if client != "default" and mc_version == "":
        raise Exception("mc_version must be give if the client is not \"default\" as string (e.g. \"1.8\" or \"1.16\")")

    developer_mode = True  # change it to True for dev mode
    if not developer_mode:
        with open(get_log(client, mc_version)[1],"r") as f:
            g = follow(f)
            for gg in g:

                found, players = extract(gg, f)

                if found:
                    yield players
    else:
        name_list = []
        while True:
            name = input("Sample names: ")
            if name == "":
                break
            else:
                name_list.append(name)

        yield name_list
