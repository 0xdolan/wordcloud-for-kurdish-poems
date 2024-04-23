#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import string
from collections import Counter
from pathlib import Path

from rich import print as rprint
from rich.progress import track

from generate_wordcloud import generate_wordcloud

CURRENT_DIR = Path().cwd()
ALLEKOK_DIR = CURRENT_DIR / "allekok"

POET_DATA_IN_TXT = ALLEKOK_DIR / "poet_data_in_TXT"
WORDCLOUDS = ALLEKOK_DIR / "wordclouds"
WORD_FREQUENCIES = ALLEKOK_DIR / "word_frequencies"


PUNCTUATION = string.punctuation + "،؛؟«»"
DIGITS = string.digits + "۰۱۲۳۴۵۶۷۸۹" + "٠١٢٣٤٥٦٧٨٩"
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

    return word


def get_word_frequency(wordlist):
    # Count the frequency of each word
    word_counts = Counter(wordlist)

    # Create a list of dictionaries containing the word and its frequency
    word_frequency_list = []
    for entry, frequency in word_counts.items():
        entry = clean_word(entry)
        if entry is not None and len(entry) >= 1:
            word_frequency_list.append({"entry": entry, "frequency": frequency})

    # sort by frequency
    word_frequency_list.sort(key=lambda x: x["frequency"], reverse=True)
    return word_frequency_list


def generate_frequencies():
    if os.path.exists(POET_DATA_IN_TXT):
        # read all files inside POET_DATA_IN_TXT directory
        for root, dirs, files in track(
            os.walk(POET_DATA_IN_TXT), description="Reading files..."
        ):
            for file in files:
                rprint(f"Generating word frequency for {file}")

                with open(os.path.join(root, file), "r", encoding="utf-8") as rf:
                    poem = rf.read().split()

                    # clear words
                    poem = [clean_word(word) for word in poem if word is not None]

                    as_json = get_word_frequency(poem)

                    with open(
                        f"{WORD_FREQUENCIES}/{file.split('.')[0]}.json",
                        "w",
                        encoding="utf-8",
                    ) as wf:
                        json.dump(
                            as_json,
                            wf,
                            ensure_ascii=False,
                            default=str,
                            allow_nan=False,
                        )

    # generate word frequency for all poems
    if os.path.exists(f"{ALLEKOK_DIR}/all_poems_concatenated.txt"):
        rprint("Gwnwrating word frequency for all poems")
        with open(
            f"{ALLEKOK_DIR}/all_poems_concatenated.txt", "r", encoding="utf-8"
        ) as rf:
            poems = rf.read().split()

        # clear words
        poems = [clean_word(word) for word in poems if word is not None]

        as_json = get_word_frequency(poems)

        with open(f"{ALLEKOK_DIR}/all_poems.json", "w", encoding="utf-8") as wf:
            json.dump(as_json, wf, ensure_ascii=False, default=str, allow_nan=False)


def generate_wordclouds():
    if os.path.exists(POET_DATA_IN_TXT):
        # read all files inside POET_DATA_IN_TXT directory
        for root, dirs, files in track(
            os.walk(POET_DATA_IN_TXT), description="Reading files..."
        ):
            for file_item in files:
                rprint(f"working on WordCloud for {file_item}")

                WORDCLOUDS.mkdir(parents=True, exist_ok=True)
                poet_dir = f"{WORDCLOUDS}/{file_item}"

                with open(os.path.join(root, file_item), "r", encoding="utf-8") as rf:
                    poem = rf.read().split()

                # clear words
                poem = [clean_word(word) for word in poem if word is not None]

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


def generate_wordclouds_for_all_poems():
    # check ./allekok/all_poems_concatenated.txt exists
    if os.path.exists(f"{ALLEKOK_DIR}/all_poems_concatenated.txt"):
        rprint("Generating WordCloud for all poems...")

        with open(
            f"{ALLEKOK_DIR}/all_poems_concatenated.txt", "r", encoding="utf-8"
        ) as rf:
            poems = rf.read().split()

        # clear words
        poems = [clean_word(word) for word in poems if word is not None]

        poems = [word for word in poems if word is not None]
        for i in range(1, 6):
            generate_wordcloud(poems, filename=f"{all_poems_dir}/wordcloud_{i}.png")

        # All words excluding one letter words
        poems = [word for word in poems if len(word) >= 1]
        for i in range(1, 6):
            generate_wordcloud(
                poems, filename=f"{all_poems_dir}/wordcloud_above_1_{i}.png"
            )

        # All words excluding one to two letter words
        poems = [word for word in poems if len(word) > 2]
        for i in range(1, 6):
            generate_wordcloud(
                poems, filename=f"{all_poems_dir}/wordcloud_above_2_{i}.png"
            )

        # All words excluding one to three letter words
        poems = [word for word in poems if len(word) > 3]
        for i in range(1, 6):
            generate_wordcloud(
                poems, filename=f"{all_poems_dir}/wordcloud_above_3_{i}.png"
            )


if __name__ == "__main__":
    # check if directories exists, if not create them and run the geneate_frequencies function
    WORD_FREQUENCIES.mkdir(parents=True, exist_ok=True)
    generate_frequencies()

    # check if directories exists, if not create them and run the generate_wordclouds function
    WORDCLOUDS.mkdir(parents=True, exist_ok=True)
    generate_wordclouds()

    # check if directories exists, if not create them and run the generate_wordclouds_for_all_poems function
    all_poems_dir = WORDCLOUDS / "all_poems"
    all_poems_dir.mkdir(parents=True, exist_ok=True)
    generate_wordclouds_for_all_poems()

    rprint("Done!")
