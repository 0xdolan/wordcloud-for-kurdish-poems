#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from rich import print as rprint
from rich.progress import track

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLEKOK = os.path.join(CURRENT_DIR, "allekok")
ALLEKOK_DIR = os.path.join(ALLEKOK, "allekok-poems")
CONCAT_AS_ONE_FILE = os.path.join(ALLEKOK, "concat_as_one_file")

# check if allekok-poems directory exists else clone from github
if not os.path.exists(ALLEKOK_DIR):
    rprint("Cloning allekok-poems from github...")
    os.system(
        f"git clone https://github.com/allekok/allekok-poems.git {ALLEKOK}/allekok-poems"
    )
    rprint("Done cloning allekok-poems")

# get list of directories inside allekok-poems
poem_dirs = [f"{ALLEKOK_DIR}/{directory}" for directory in os.listdir(ALLEKOK_DIR)]

# get list of poets
poets = sorted([x for x in os.listdir(poem_dirs[6]) if not "index.html" in x])

# get full path of each poem
poem_full_paths = [os.path.join(poem_dirs[6], poem) for poem in poets]
rprint(f"Read {len(poem_full_paths)} poems directories from {poem_dirs[6]}")


def get_all_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_list.append(filepath)
    return file_list


def extract_poem(poem):
    for poet in poets:
        for path in track(poem_full_paths, description=f"Reading {poet}s' poems..."):
            base_name = os.path.basename(path)
            if poet == base_name:
                for file_path in get_all_files(path):
                    if file_path.endswith(".html"):
                        continue
                    with open(file_path, "r", encoding="utf-8") as rf, open(
                        f"{CONCAT_AS_ONE_FILE}/{base_name}", "a", encoding="utf-8"
                    ) as wf:
                        for line in rf:
                            if any(
                                [
                                    x in line
                                    for x in [
                                        "شاعیر:",
                                        "کتێب:",
                                        "سەرناو:",
                                        "لەبارەی شیعر:",
                                    ]
                                ]
                            ):
                                continue
                            wf.write(line + "\n")


def concat_all_poems():
    """Read all poems and concat them into one file"""

    for root, dirs, files in track(os.walk(f"{ALLEKOK}/concat_as_one_file")):
        rprint(f"Reading files from {root}...")
        rprint(f"Found {len(files)} files")
        all_poems = f"{ALLEKOK}/all_poems.txt"
        for file in files:
            rprint(f"Reading {file}...")
            with open(
                f"{CONCAT_AS_ONE_FILE}/{file}", "r", encoding="utf-8"
            ) as rf, open(all_poems, "a", encoding="utf-8") as wf:
                for line in rf:
                    # remove empty lines and lines with only whitespace
                    if not line.strip() or line.strip() == "":
                        continue

                    wf.write(line + "\n")
    rprint(f"Done writing all poems to {all_poems}")


if __name__ == "__main__":
    # check if allekok directory exists, if not create it
    if not os.path.exists("./allekok"):
        os.mkdir("./allekok")

    if not os.path.exists(CONCAT_AS_ONE_FILE):
        os.mkdir(CONCAT_AS_ONE_FILE)
        extract_poem(poem_full_paths)
    else:
        rprint("Concat_as_one_file directory exists, skipping...")

    if not os.path.exists(f"{ALLEKOK}/all_poems.txt"):
        concat_all_poems()
    else:
        rprint("all_poems.txt exists, skipping...")

    rprint("Cleaning up all_poems.txt...")
    subprocess.run(["chmod", "+x", "./clean.sh"])
    subprocess.run(["./clean.sh"])
    rprint("Done!")
