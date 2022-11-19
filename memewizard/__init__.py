"""
memewizard
~~~~~~~~~~
One good source for all things memes
    >>> from memewizard import meme_object_yt
    >>> from memewizard.cli import main
    >>> from memewizard.visual import make_pie
"""

import json
import random
import re
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytrends.request
import requests
from bs4 import BeautifulSoup
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from memewizard.helpers import chunkify, subjectify

warnings.filterwarnings("ignore")
stopwords = [
    "Why Is",
    "Why Does",
    "Everyone",
    "EVERYONE",
    "Why",
    "Is The",
    "How",
    "What Are",
    "What's Up",
    "With",
    "?",
    ".",
    "Are You",
    "FINISHED",
]


def funnywords() -> "list[str]":
    words = requests.get(
        "https://raw.githubusercontent.com/snguyenthanh/better_profanity/master/better_profanity/profanity_wordlist.txt"
    ).text.split("\n")
    while "" in words:
        words.remove("")
    return words


regex = re.compile("|".join(map(re.escape, stopwords)))
nsfw_regex = re.compile("|".join(funnywords()) + "|rule 34|b*tches|d*ck", re.IGNORECASE)


class meme_object:
    """The meme_object class to handle KnowYourMeme data"""

    def fetch_memes(page: str) -> list:
        """Scrape any memes page on knowyourmemes.com"""

        r = requests.get(
            "https://knowyourmeme.com/memes/page/{}".format(page),
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            },
        ).text
        soup = BeautifulSoup(r, "html.parser")

        # parsing perfection
        m = soup.find("tbody", {"class": ["entry-grid-body", "infinite"]}).text.split(
            "    "
        )

        for i, s in enumerate(m):
            m[i] = s.strip()
            if m[i] == "":
                del m[i]
        for i, s in enumerate(m):
            m[i] = s.strip()
        for i, s in enumerate(m):
            if "NSFW" in m[i] or m[i] == "NSFW":
                del m[i + 1]
                del m[i]
        while "" in m:
            m.remove("")
        for i, s in enumerate(m):
            if "Updated" in m[i]:
                del m[i]

        return [i.strip() for i in m if not nsfw_regex.search(i)]

    def fetch_meme_info(url: str) -> dict:
        """Fetch more information on a meme with a given URL."""
        r = requests.get(
            url,
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            },
        )
        s = BeautifulSoup(r.text, "html.parser")
        title = s.find("title").text.split(" |")[0]

        try:
            st = s.find("div", {"class": ["details"]}).text.split("\n\n")
        except AttributeError:
            st = [""]
        while "" in st:
            st.remove("")
        st = [_st.replace(":", "").replace("\n", "") for _st in st]
        st = list(chunkify(st, 2))
        st.insert(0, ["Name", title])

        if invalids.RESEARCH in st:
            st.remove(invalids.RESEARCH)
        return {title: st}

    def fetch_meme_images(meme_list: list) -> list:
        """Find relevant images for a list of memes."""
        meme_images = []
        for meme in meme_list:
            r = requests.get(
                "https://www.google.com/search?q={}&rlz=1CAOUAQ_enUS980&source=lnms&tbm=isch&biw=1517&bih=750&dpr=0.9&surl=1&safe=active&ssui=on#imgrc=1QhXmjkgq_MRQM".format(
                    meme
                )
            ).text
            soup = BeautifulSoup(r, "html.parser")

            images = soup.find_all("img")
            meme_images.append(images[random.randrange(1, len(images))]["src"])

        return meme_images

    def fetch_trend_history(memes: list) -> list:
        """Fetch trend history of a given list of memes. The list of memes should contain less than 6 items."""
        trend = pytrends.request.TrendReq()
        trend.build_payload(memes, timeframe="today 1-m", cat="0", geo="US")

        search = trend.interest_over_time()

        df = pd.DataFrame(search)
        df.reset_index(inplace=True, drop=True)
        df = df.to_dict()

        meme = []
        for k in df:
            submeme = []
            v = df[k]
            for e in v:
                if not isinstance(v[e], (bool, str)):
                    submeme.append(v[e])
            meme.append(submeme)
        while [] in meme:
            meme.remove([])

        return meme


class meme_object_yt:
    """The meme_object class to handle data from YouTube"""

    def fetch_memes() -> list:
        """Fetches memes from LessonsInMemeCulture on YouTube and does a ton of parsing magic."""
        r = requests.get("https://www.youtube.com/c/LessonsinMemeCulture/videos")
        big_response = json.loads(
            r.text.split("var ytInitialData =")[1].split(";</script>")[0]
        )
        filtere = big_response["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1][
            "tabRenderer"
        ]["content"]["richGridRenderer"]["contents"]
        res = []
        for i in range(len(filtere)):
            try:
                string = (
                    filtere[i]["richItemRenderer"]["content"]["videoRenderer"]["title"][
                        "runs"
                    ][0]["text"]
                    .replace("“", '"')
                    .replace("”", '"')
                )
                token = regex.sub("", string)
                words = re.findall('"([^"]*)"', string)
                if len(words) > 0:
                    meme = "".join([s.split("_")[0] for s in words[0]])
                    res.append(meme)
                else:
                    res.append(subjectify(token))
            except KeyError:
                break

        print(res)
        return res

    def fetch_meme_dates() -> list:
        """Fetch "meme" dates from LessonsInMemeCulture"""
        r = requests.get("https://www.youtube.com/c/LessonsinMemeCulture/videos")
        big_response = json.loads(
            r.text.split("var ytInitialData =")[1].split(";</script>")[0]
        )
        filtere = big_response["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1][
            "tabRenderer"
        ]["content"]["richGridRenderer"]["contents"]

        print(filtere[0])
        dates = []

        for i in range(len(filtere)):
            try:
                dates.append(
                    filtere[i]["richItemRenderer"]["content"]["videoRenderer"][
                        "publishedTimeText"
                    ]["simpleText"]
                )
            except KeyError:
                break
        return dates


class invalids:
    RESEARCH = [
        "This submission is currently being researched and evaluated.",
        "You can help confirm this entry by contributing facts, media, and other evidence of notability and mutation.",
    ]
    NOTFOUND = "Page Not Found (404) - Know Your Meme"
    GALLERY = "Trending Videos Gallery"


def predict(meme: str) -> None:
    """Predict the popularity of a meme"""
    memes = meme_object.fetch_trend_history([meme])[0]
    data = [[i, m] for i, m in enumerate(memes)]

    y_data = np.array(data)[:, 1]

    X = np.array(range(len(y_data))).reshape(-1, 1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_data, test_size=0.25, random_state=0
    )

    logreg = LogisticRegression(solver="lbfgs", max_iter=1000)
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)

    y = [*y_train, *y_test, *y_pred]

    plt.plot(range(len(y)), y, c="black")
    plt.axvline(len(y) - len(y_pred), c="blue", alpha=0.2)
    plt.title("History for '{}'".format(meme))

    plt.savefig("figure.png")
