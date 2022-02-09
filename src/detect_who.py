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


def main(client = "default", mc_version = ""):

    """
    Available clients:
    - default
    - lunar

    mc_version must be give if the client is not "default" as string (e.g. "1.8" or "1.16")
    """

    if client != "default" and mc_version == "":
        raise Exception("mc_version must be give if the client is not \"default\" as string (e.g. \"1.8\" or \"1.16\")")

    with open(get_log(client, mc_version)[1],"r") as f:
        g = follow(f)
        for gg in g:
            
            if "[Client thread/INFO]: [CHAT] ONLINE: " in gg:
                msg = gg.split("ONLINE: ")[1]
                players = msg.split(", ")
                if " [x" in players[len(players)-1]:
                    players[len(players)-1] = players[len(players)-1].split(" [x")[0]
                yield players


if __name__ == "__main__":
    g = main("lunar", "1.8")
    for gg in g:
        print(gg)