"""Functions that all relate to visualization"""

import http.server
import json
import os
import socketserver
import statistics
import webbrowser

import requests
from html2image import Html2Image

import memewizard
from memewizard.helpers import chunkify, color, colors


def make_pie():
    doc = requests.get(
        "https://raw.githubusercontent.com/ajskateboarder/stuff/main/meme.js/pie.html"
    ).text
    page = [
        meme.strip()
        for meme in memewizard.meme_object_yt.fetch_memes()
        if not memewizard.nsfw_regex.search(meme)
    ]
    resp = {}
    for sn in page:
        s = memewizard.meme_object.fetch_trend_history([sn])
        try:
            resp[sn] = statistics.mean(s[0])
        except IndexError:
            pass

    data, colours = json.dumps(resp).replace("{", "").replace("}", ""), str(
        colors(len(resp))
    ).replace("[", "").replace("]", "")

    open("document.html", "w").write(
        doc.replace("/*data*/", data).replace("/*colors*/", colours)
    )
    Html2Image(
        custom_flags=["--virtual-time-budget=5000", "--default-background-color=0"]
    ).screenshot(html_file="document.html", save_as="chart.png", size=(600, 600))
    show = input(
        color.BOLD
        + color.BLUE
        + "Would you like to keep the document.html used by the program? [Y/n] "
        + color.END
    )

    if show.lower() == "n":
        os.remove("document.html")


def make_trackback_pie(serve=False):
    if not os.path.exists("bin/"):
        os.mkdir("bin")

    def pies_():
        memes = memewizard.meme_object_yt.fetch_memes()
        resp = []
        for meme in memes:
            try:
                if not any(ele in meme.strip() for ele in memewizard.funnywords()):
                    resp.append(
                        [
                            {meme.strip(): round(statistics.mean(s))}
                            for s in list(
                                chunkify(
                                    memewizard.meme_object.fetch_trend_history([meme])[
                                        0
                                    ],
                                    3,
                                )
                            )
                        ]
                    )
            except IndexError:
                pass
        return resp

    def pies():
        p = pies_()
        resp = []
        for i in range(len(p)):
            timeframe = {}
            for l in p:
                try:
                    timeframe[list(l[i].keys())[0]] = list(l[i].values())[0]
                except IndexError:
                    pass
            resp.append(timeframe)
        return resp

    data = pies()
    doc = requests.get(
        "https://raw.githubusercontent.com/ajskateboarder/stuff/main/meme.js/pie.html"
    ).text
    colours = str(colors(len(data))).replace("[", "").replace("]", "")

    os.chdir("bin")
    for i, datum in enumerate(data):
        resp = json.dumps(datum).replace("{", "").replace("}", "")
        open(f"chart{i}.html", "w").write(
            doc.replace("/*data*/", resp).replace("/*colors*/", colours)
        )
        Html2Image(
            output_path="images",
            custom_flags=["--virtual-time-budget=5000", "--default-background-color=0"],
        ).screenshot(
            html_file=f"chart{i}.html", save_as=f"chart{i}.png", size=(600, 600)
        )

    open("index.html", "w").write(
        requests.get(
            "https://raw.githubusercontent.com/ajskateboarder/stuff/main/meme.js/trackpie.html"
        ).text
    )
    if serve == True:
        with socketserver.TCPServer(
            ("", 5000), http.server.SimpleHTTPRequestHandler
        ) as httpd:
            print("Opening visualization on http://localhost:5000...")
            webbrowser.open("http://localhost:5000")
            httpd.serve_forever()
