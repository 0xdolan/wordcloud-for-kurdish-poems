#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import matplotlib
import matplotlib.pyplot as plt
from rich import print as rprint
from wordcloud import WordCloud

matplotlib.use("Agg")

GITHUB_FONT_PATH = "https://github.com/rastikerdar/vazirmatn/blob/master/fonts/ttf/Vazirmatn-Regular.ttf?raw=true"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(CURRENT_DIR, "allekok/fonts")

# if font directory is not exist, create it and download the font file from github
if not os.path.exists(FONT_DIR):
    os.mkdir(FONT_DIR)
    rprint("Downloading Vazirmatn-Regular.ttf from github...")
    os.system(f"wget -q -O {FONT_DIR}/Vazirmatn-Regular.ttf {GITHUB_FONT_PATH}")


VAZIRMATN_FONT_PATH = os.path.join(CURRENT_DIR, f"{FONT_DIR}/Vazirmatn-Regular.ttf")


def generate_wordcloud(text, filename="wordcloud.png"):
    wc = WordCloud(
        font_path=VAZIRMATN_FONT_PATH,
        width=1600,
        height=800,
        background_color="white",
    )
    if isinstance(text, list):
        text = " ".join(text)

    wc.generate(text)

    plt.axis("off")
    plt.figure(figsize=(20, 10))
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig(filename, facecolor="k", bbox_inches="tight")
    # plt.show()
    plt.close()
