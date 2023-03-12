#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import matplotlib
import matplotlib.pyplot as plt
from rich import print as rprint
from wordcloud import WordCloud

matplotlib.use("Agg")

GITHUB_FONT_PATH = "https://github.com/rastikerdar/vazirmatn/blob/master/fonts/ttf/Vazirmatn-Regular.ttf?raw=true"

# if font directory is not exist, create it and download the font file from github
if not os.path.exists("fonts"):
    os.mkdir("fonts")
    rprint("Downloading Vazirmatn-Regular.ttf from github...")
    os.system(f"wget -O ./fonts/Vazirmatn-Regular.ttf {GITHUB_FONT_PATH}")


VAZIRMATN_FONT_PATH = os.path.join(os.getcwd(), "fonts/Vazirmatn-Regular.ttf")


def generate_wordcloud(wordlist, filename="wordcloud.png"):
    wc = WordCloud(
        font_path=VAZIRMATN_FONT_PATH,
        width=1600,
        height=800,
        background_color="white",
    )
    wc.generate(" ".join(wordlist))

    plt.axis("off")
    plt.figure(figsize=(20, 10))
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig(filename, facecolor="k", bbox_inches="tight")
    # plt.show()
    plt.close()
