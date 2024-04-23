#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Source of the Poems: https://github.com/allekok/allekok-poems.git

import json
import os
import re
import subprocess
from pathlib import Path

from rich import print as rprint
from rich.progress import track

CURRENT_DIR = Path(__file__).resolve().parent
ALLEKOK_DIR = CURRENT_DIR / "allekok"
CONCAT_AS_ONE_FILE = ALLEKOK_DIR / "concat_as_one_file"
POET_DATA_IN_JSON = ALLEKOK_DIR / "poet_data_in_JSON"


def get_all_files(directory_path):
    all_files = []
    directory = Path(directory_path)
    for file_path in directory.rglob("*"):
        if file_path.is_file():
            all_files.append(file_path)
    return all_files


def normalized_text():
    data = []
    if POET_DATA_IN_JSON.is_dir():
        # total_poets = len(list(POET_DATA_IN_JSON.iterdir()))
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

                    # # Create a directory for each poet if it doesn't exist
                    # poet_dir = ALLEKOK_DIR / "TXT_VERSIONS" / poet.replace(" ", "_")
                    # poet_dir.mkdir(parents=True, exist_ok=True)

                    # # Write the concatenated text to a text file
                    # output_file = (
                    #     poet_dir
                    #     / f"{poet.replace(' ', '_')}_{book.replace(' ', '_')}.txt"
                    # )
                    # with open(output_file, "w", encoding="utf-8") as f:
                    #     f.write(concat_text)

                    data.append(
                        {
                            "poet": poet,
                            "poet_description": poet_description,
                            "total_poets": len(file_data),
                            "concat_text": "\n".join(texts),
                        }
                    )
    return data


with open(ALLEKOK_DIR / "all_poems_concatenated.txt", "w", encoding="utf-8") as wf:
    rprint("Consolidating all poems into a single file: `all_poems_concatenated.txt`")
    for item in track(normalized_text(), "Processing..."):
        wf.write(item.get("concat_text", ""))


def clean_all_poems_concatenated(directory):
    # Check if the input file exists
    input_file = directory / "all_poems_concatenated.txt"
    if input_file.is_file():
        clean_script = CURRENT_DIR / "clean.sh"
        clean_script.chmod(0o755)  # Ensure the script is executable = chmod +x clean.sh
        # Run the cleaning script
        rprint("Cleaning the concatinated poems...")
        subprocess.run([clean_script])
        rprint(
            "The file has been successfully cleaned and saved as `all_poems_concatenated_cleaned.txt`."
        )
    else:
        rprint(
            f"Warning: File 'all_poems_concatenated.txt' not found in {directory}. Cleaning skipped."
        )


if __name__ == "__main__":
    clean_all_poems_concatenated(ALLEKOK_DIR)
