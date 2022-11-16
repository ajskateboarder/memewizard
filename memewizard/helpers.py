"""Good ol helpers"""

import random
import re

trails = ("classic", "everywhere")


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREY = "\033[90m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def colors(amount):
    return [
        rgb_to_hex(
            (
                random.randrange(200, 255),
                random.randrange(200, 255),
                random.randrange(200, 255),
            )
        )
        for _ in range(amount)
    ]


def subjectify(text):
    _list = re.split(r"{}".format("|".join(trails)), "".join(text), flags=re.IGNORECASE)
    return "".join(_list)


def chunkify(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]
