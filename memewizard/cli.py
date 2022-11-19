#!/usr/bin/env python3

"""The command line functions"""

import traceback
import webbrowser

import requests
from bs4 import BeautifulSoup
from InquirerPy import prompt
from tabulate import tabulate

import memewizard
from memewizard.helpers import color
from memewizard.visual import make_pie, make_trackback_pie


def main() -> None:
    """The cool CLI function that you definitely use"""

    print(
        "\x1b[32m\x1b[1m",
        """
  . * .
     .  *                                 _                  _
   . *. * .                              (_)                | |
   _ __ ___   ___ _ __ ___   _____      ___ ______ _ _ __ __| |
  | '_ ` _ \ / _ \ '_ ` _ \ / _ \ \ /\ / / |_  / _` | '__/ _` |
  | | | | | |  __/ | | | | |  __/\ V  V /| |/ / (_| | | | (_| |
  |_| |_| |_|\___|_| |_| |_|\___| \_/\_/ |_/___\__,_|_|  \__,_|
  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
  version 0.0.5.1
  """,
        "\x1b[0m",
    )
    selection = prompt(
        [
            {
                "type": "list",
                "name": "choice",
                "message": "What do you want to do?",
                "choices": [
                    "Create a meme popularity pie chart",
                    "Fetch information for a single meme",
                    "Exit",
                ],
            }
        ]
    )

    if selection["choice"] == "Create a meme popularity pie chart":
        selection = PyInquirer.prompt(
            [
                {
                    "type": "list",
                    "name": "choice",
                    "message": "What kind of pie do you want to make?",
                    "choices": [
                        "Make a single pie for current information",
                        "Make multiple pies going back 30 days",
                    ],
                }
            ]
        )
        if selection["choice"] == "Make a single pie for current information":
            make_pie()
            exit(0)
        else:
            make_trackback_pie(serve=True)
    elif selection["choice"] == "Fetch information for a single meme":
        memesyt, historyyt = (
            memewizard.meme_object_yt.fetch_memes(),
            memewizard.meme_object_yt.fetch_meme_dates(),
        )
        memesyt = [
            meme.strip() for meme in memesyt if not memewizard.nsfw_regex.search(meme)
        ]

        print(
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            + "\n".join(
                [
                    "{}. {}{}{}  {}{}{}".format(
                        i, color.BOLD, a, color.END, color.GREY, b, color.END
                    )
                    for i, (a, b) in enumerate(zip(memesyt, historyyt))
                ]
            )
            + "\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
        )
        while True:
            x = input(
                color.BOLD
                + color.BLUE
                + "Select a meme by its number (add ? after number for meme images) > "
                + color.END
            )
            try:
                if x.endswith("?") and x.count("?") == 1:
                    try:
                        x = int(x.replace("?", ""))
                        webbrowser.open(
                            "https://duckduckgo.com/?q={}".format(memesyt[x])
                        )
                    except ValueError:
                        print(
                            color.RED
                            + "Not a number. Please use a real number that is in range."
                            + color.END
                        )
                else:
                    doc = requests.get(
                        "https://www.google.com/search?q={}&surl=1&safe=active&ssui=on".format(
                            str(memesyt[int(x)] + " know your meme").replace(" ", "+")
                        )
                    )
                    soup = BeautifulSoup(doc.text, "html.parser")

                    search = [
                        link["href"]
                        for link in soup.find_all("a", href=True)
                        if "knowyourmeme.com" in link["href"]
                        and link["href"].find("cultures") == -1
                    ][0]

                    data = memewizard.meme_object.fetch_meme_info(
                        search.split("url?q=")[1].split("&sa")[0].replace("25", "")
                    )
                    key = list(data.keys())[0]
                    if (
                        memewizard.invalids.NOTFOUND in key
                        or memewizard.invalids.GALLERY in key
                    ):
                        print(
                            color.RED
                            + "What!? That meme does not exist in the KnowYourMeme database."
                            + color.END
                        )
                    else:
                        if len(data[key]) < 5:
                            print(
                                color.YELLOW
                                + "It looks like there is limited data for this meme. You may encounter errors."
                                + color.END
                            )
                        print(
                            color.BOLD
                            + "Most related meme"
                            + color.END
                            + "\n"
                            + tabulate(data[key])
                        )
                        y = input(
                            color.BOLD
                            + color.BLUE
                            + "Would you like to view the Google Search trend history for this meme ({}) [Y/n] ? ".format(
                                key
                            )
                            + color.END
                        )
                        if y == "n" or y == "N":
                            pass
                        else:
                            try:
                                print(
                                    color.BOLD
                                    + 'Saving trend history to "figure.png"...'
                                    + color.END,
                                    end="",
                                    flush=True,
                                )
                                memewizard.predict(key)
                                print(
                                    "\r"
                                    + color.BOLD
                                    + 'Saving trend history to "figure.png"...'
                                    + color.END
                                    + " Finished\n",
                                    end="",
                                    flush=True,
                                )
                            except Exception as e:
                                print(
                                    "\n"
                                    + color.BOLD
                                    + color.RED
                                    + "An error has occurred. The stack trace has been logged for further details.\n\n"
                                    + traceback.format_exc()
                                    + color.END
                                )
                            exit(0)
            except ValueError:
                print(
                    color.RED
                    + "Not a number. Please use a real number that is in range."
                    + color.END
                )
    else:
        exit(0)


if __name__ == "__main__":
    main()
