#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Source of the Poems: https://github.com/allekok/allekok-poems.git

import json
import re
import string
from pathlib import Path

from rich import print as rprint
from rich.progress import track

CURRENT_DIR = Path(__file__).resolve().parent
ALLEKOK_DIR = CURRENT_DIR / "allekok"
CONCAT_AS_ONE_FILE = ALLEKOK_DIR / "concat_as_one_file"
POET_DATA_IN_JSON = ALLEKOK_DIR / "poet_data_in_JSON"


PUNCTUATION = string.punctuation + "،؛؟«»"
DIGITS = string.digits + "۰۱۲۳۴۵۶۷۸۹" + "٠١٢٣٤٥٦٧٨٩"
WHITESPACE = string.whitespace


def get_all_files(directory_path):
    all_files = []
    directory = Path(directory_path)
    for file_path in directory.rglob("*"):
        if file_path.is_file():
            all_files.append(file_path)
    return all_files


def remove_patterns(text):

    word = word.strip()
    # remove digits
    word = word.strip(DIGITS)
    # remove punctuation
    word = word.strip(PUNCTUATION)
    # remove newlines
    word = word.strip(WHITESPACE)

    patterns = [
        r"^$",
        r"[\t\nـ*٭•+\-\=]+",
        r"[۰١٢٣٤٥٦٧٨٩1234567890٠١٢٣٤٥٦٧٨٩\t\(\)\.]+",
    ]
    combined_pattern = re.compile("|".join(patterns), re.M)
    cleaned_text = re.sub(combined_pattern, "", text)
    return cleaned_text


def normalized_text():
    data = []
    if POET_DATA_IN_JSON.is_dir():
        all_json_files = get_all_files(POET_DATA_IN_JSON)
        for json_file in all_json_files:

            # Load the JSON data from the file
            with open(json_file, "r") as json_file:
                file_data = json.load(json_file)
                texts = []
                for item in file_data:
                    poet = item.get("poet", "")
                    poet_description = item.get("poet_description", "")
                    book = item.get("book", "")
                    poem_title = item.get("poem_title", "")
                    poem_description = item.get("poem_description", "")
                    poem_text = item.get("poem_text", "")

                    concat_text = (
                        f"{book}\n{poem_title}\n{poem_description}\n{poem_text}"
                    )
                    texts.append(concat_text)

                    data.append(
                        {
                            "poet": poet,
                            "poet_description": poet_description,
                            "total_poets": len(file_data),
                            "concat_text": "\n".join(texts),
                        }
                    )
    return data


def concat_to_one():
    # Concatinate all poems related to each poet
    rprint("Concatinate all poems related to each poet")
    poem_data = dict()
    for item in normalized_text():
        poet_name = item.get("poet", "").strip().replace(" ", "_")
        if poet_name not in poem_data:
            poem_data[poet_name] = []
        poem_data[poet_name].append(item.get("concat_text", ""))

    for poet_name, poems in track(poem_data.items(), "Processing..."):
        # Create a directory for each poet if it doesn't exist
        poet_dir = ALLEKOK_DIR / Path("poet_data_in_TXT") / poet_name
        poet_dir.mkdir(parents=True, exist_ok=True)

        # all_poems_concatenated = remove_patterns("\n".join(poems))
        all_poems_concatenated = "\n".join(poems)
        file_path = poet_dir / f"{poet_name}.txt"
        if not Path(ALLEKOK_DIR / poet_dir).is_file():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(all_poems_concatenated)


def concat_for_each_poet():
    # Concatinate all the poems into single one
    with open(ALLEKOK_DIR / "all_poems_concatenated.txt", "w", encoding="utf-8") as wf:
        rprint(
            "Consolidating all poems into a single file: `all_poems_concatenated.txt`"
        )
        for item in track(normalized_text(), "Processing..."):
            # wf.write(remove_patterns(item.get("concat_text", "")))
            wf.write(item.get("concat_text", ""))


if __name__ == "__main__":
    concat_to_one()
    concat_for_each_poet()
