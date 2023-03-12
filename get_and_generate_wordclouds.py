#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import string
from collections import Counter

from rich import print as rprint
from rich.progress import track

from generate_wordcloud import generate_wordcloud

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PUNCTUATION = string.punctuation
DIGITS = string.digits
WHITESPACE = string.whitespace


def clean_word(word):
    # check if not None
    if word is None:
        return None
    # remove leading and trailing spaces
    word = word.strip()
    # remove digits
    word = word.strip(DIGITS)
    # remove punctuation
    word = word.strip(PUNCTUATION)
    # remove newlines
    word = word.strip(WHITESPACE)
    # remove empty strings
    if word != "":
        return word


def get_word_frequency(word_list):
    # Count the frequency of each word
    word_counts = Counter(word_list)

    # Create a list of dictionaries containing the word and its frequency
    word_frequency_list = []
    for entry, frequency in word_counts.items():
        entry = clean_word(entry)
        word_frequency_list.append({"entry": entry, "frequency": frequency})

    # sort by frequency
    word_frequency_list.sort(key=lambda x: x["frequency"], reverse=True)
    return word_frequency_list


CONCAT_AS_ONE_FILE = os.path.join(CURRENT_DIR, "concat_as_one_file")
WORDCLOUDS = os.path.join(CURRENT_DIR, "wordclouds")
WORD_FREQUENCIES = os.path.join(CURRENT_DIR, "word_frequencies")

# check if above directories exist, if not create them
if not os.path.exists(WORDCLOUDS):
    os.mkdir(WORDCLOUDS)
if not os.path.exists(WORD_FREQUENCIES):
    os.mkdir(WORD_FREQUENCIES)
if not os.path.exists(CONCAT_AS_ONE_FILE):
    os.mkdir(CONCAT_AS_ONE_FILE)


def main():
    if os.path.exists(CONCAT_AS_ONE_FILE):
        # read all files inside CONCAT_AS_ONE_FILE directory
        for root, dirs, files in track(
            os.walk(CONCAT_AS_ONE_FILE), description="Reading files..."
        ):
            for file in files:
                rprint(f"working on word frequency for {file}")

                with open(os.path.join(root, file), "r", encoding="utf-8") as rf:
                    poem = rf.read().split()

                    # clear words
                    poem = [clean_word(word) for word in poem]

                    as_json = get_word_frequency(poem)

                    with open(
                        f"{WORD_FREQUENCIES}/{file}.json", "w", encoding="utf-8"
                    ) as wf:
                        json.dump(
                            as_json, wf, indent=4, ensure_ascii=False, default=str
                        )

                rprint(f"working on WordCloud for {file}")
                poet_dir = f"{WORDCLOUDS}/{file}"

                # make sure wordclouds directory exists, if not create it
                if not os.path.exists(poet_dir):
                    os.mkdir(poet_dir)

                    # All words including one letter words
                    poem = [word for word in poem if word is not None]
                    for i in range(1, 6):
                        generate_wordcloud(
                            poem, filename=f"{poet_dir}/wordcloud_{i}.png"
                        )

                    # All words excluding one letter words
                    poem = [word for word in poem if len(word) > 1]
                    for i in range(1, 6):
                        generate_wordcloud(
                            poem, filename=f"{poet_dir}/wordcloud_above_1_{i}.png"
                        )

                    # All words excluding one to two letter words
                    poem = [word for word in poem if len(word) > 2]
                    for i in range(1, 6):
                        generate_wordcloud(
                            poem, filename=f"{poet_dir}/wordcloud_above_2_{i}.png"
                        )

                    # All words excluding one to three letter words
                    poem = [word for word in poem if len(word) > 3]
                    for i in range(1, 6):
                        generate_wordcloud(
                            poem, filename=f"{poet_dir}/wordcloud_above_3_{i}.png"
                        )


if __name__ == "__main__":
    main()
    rprint("DONE")
