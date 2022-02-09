# What it does

This collects all player names of the players who are playing in your Hypixel round (e.g. Bedwars, SkyWars, ...) and collects all their data using the Hyixel api, filters it and prints it into the console.

# This only works for Bedwars yet!

# Usage

- Run main.py in terminal
- Enter your Hypixel api key (you can optain it by using /key on the server)
- Enter the launcher you are using (The default and Lunarclient are supported)
- Enter the minecraft version you are using (if asked)
- Use /who as soon as you joined a game

## Important

By default the results will be printed filtered by ```filters.json``` you can/should change that to your own preferences.

### The filter

#### Introduction

The Hypixel api returns a very huge and confusing string of data for what reason it was necessary to filter the result. The filter is setup in a way it can be changed easley.
The filter is stored in ```src/filters.json```.

#### Changing the filter

You change the filter by editing ```src/filters.json``` as described below.  

Looking at an example:  
With this data we want to filter (this is how a api response of the player XXX could look like):

```json
{
    "success": true,
    "player": {
        "playername": "XXX",

        "a_lot_of_stuff": {
        },
        "stats": {
            "Bedwars": {
                "Experience": 12345,
                "wins_bedwars": 0,
                "losses_bedwars": 5,
                "eight_two_losses_bedwars": 3,
                "kills_bedwars": 20,

                "stuff_we_dont_want":
                [
                    "asdf",
                    "a",
                    "b"
                ]
            },
            "SkyWars": {
                "games_played_skywars": 45,
                "quits": 13,
                "chests_opened": 10
            }
        },
    "mostRecentGameType": "BEDWARS"
    }
}
```

And this filter:

```json
{                                       <- notice there is no need for the "player" key
    "stats": {                          <- key1 (must be in data)
        "Bedwars": {                    <- key2 (must be in data)
            "Overall": [                <- this key is only for structure and orientation (does not filter anything)
                "Experience",           <- key3 (must be under key1 and key2)
                "wins_bedwars",
                "losses_bedwars",
                "winstreak",            
                "final_kills_bedwars",
                "final_deaths_bedwars",
                "games_played_bedwars"
            ],
            "Kills and deaths": [
                "kills_bedwars",
                "deaths_bedwars"
            ]
        },
        "SkyWars": {
            "some_random_name": [
                "quits"
            ]
        }
    }
}
```

Results into this:

```json
{
    "XXX": {
                                <- the "player" key does not appear because it is unnecessary
        "stats": {
            "Bedwars": {
                "Overall": {
                    "Experience": 12345,
                    "wins_bedwars": 0,
                    "losses_bedwars": 5,
                    "winstreak": null,              <- null because it is not present in the data with the keys "stats", "Bedwars", "winstreak"
                    "final_kills_bedwars": null,
                    "final_deaths_bedwars": null,
                    "games_played_bedwars": null
                },
                "Kills and deaths": {
                    "kills_bedwars": 20,
                    "deaths_bedwars": null
                }
            },
            "SkyWars": {
                "some_random_name": {
                    "quits": 13
                }
            }
        }
    }
}
```

And will be printed as so:

```text
XXX:
 | Overall:                         <- you see only this because it tries to filter the relevant information (based on the game you are playing)
 |  | Experience: 12345
 |  | wins_bedwars: 0
 |  | losses_bedwars: 5
 |  | winstreak: null
 |  | final_kills_bedwars: null
 |  | final_deaths_bedwars: null
 |  | games_played_bedwars: null
 | 
```

For the key names you can have a look at [```example_response.json```](example_resoponse.json)
