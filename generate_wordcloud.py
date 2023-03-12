#!/usr/bin/env python
# -*- coding: utf-8 -*-


import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud

matplotlib.use("Agg")

VAZIR_FONT_PATH = "https://github.com/rastikerdar/vazirmatn/blob/master/fonts/ttf/Vazirmatn-Regular.ttf?raw=true"


def generate_wordcloud(wordlist, filename="wordcloud.png"):
    wc = WordCloud(
        font_path=VAZIR_FONT_PATH,
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
