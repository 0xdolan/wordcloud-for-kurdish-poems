#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import os
import sqlite3
from pathlib import Path

CURRENT_DIR = Path().cwd()
ALLEKOK_DIR = CURRENT_DIR / "allekok"
DB_FILE = ALLEKOK_DIR / "allekok.db"
ALLEKOK_TABLE_NAMES = ["poetmodel", "bookmodel", "poemmodel"]

# for table in get_table_names_of_the_table(DB_FILE):
#     print(table, get_table_column_names(DB_FILE, table))

# poetmodel -> About the poets
# poetmodel =>  ['id', 'full_name', 'view', 'surname', 'name', 'description']

# bookmodel -> About the books
# bookmodel =>  ['id', 'name', 'view', 'poet_id']

# poemmodel -> About the poems
# poemmodel =>  ['id', 'name', 'text', 'description', 'lang', 'tag', 'link', 'view', 'book_id']


# Execute a query to get the list of tables
def get_table_names_of_the_table(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    return table_names


# Get Table Column Name
def get_table_column_names(db_name, table_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info({})".format(table_name))
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    connection.close()
    return column_names


# Get Table Rows
def get_table_rows(db_name, table_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    connection.close()
    return rows


poems = get_table_rows(DB_FILE, "poemmodel")
books_data = get_table_rows(DB_FILE, "bookmodel")
poets_data = get_table_rows(DB_FILE, "poetmodel")

for poet in poets_data:
    poet_poems_books = []

    poet_id = poet[0]
    poet_name = poet[1].strip()
    poet_description = poet[-1].strip()

    # Create a folder for the current poet
    poet_folder_path = (
        ALLEKOK_DIR / Path("poet_data_in_JSON") / poet_name.replace(" ", "_")
    )
    poet_folder_path.mkdir(parents=True, exist_ok=True)

    for poem in poems:
        book_id = poem[-1]
        for book in books_data:
            if book_id == book[0]:
                if book[-1] == poet_id:  # Check if the book belongs to the current poet
                    data = {
                        "poet": poet_name.strip(),
                        "poet_description": poet_description.strip(),
                        "book": book[1].strip(),
                        "poem_title": poem[1].strip(),
                        "poem_description": poem[3].strip(),
                        "poem_text": poem[2].strip(),
                    }
                    poet_poems_books.append(data)

    # Save the poet's data as a JSON file inside the folder
    poet_json_file = f"{poet_name.replace(' ', '_')}.json"
    poet_json_path = os.path.join(poet_folder_path, poet_json_file)
    with open(poet_json_path, "w", encoding="utf-8") as json_file:
        json.dump(poet_poems_books, json_file, ensure_ascii=False)

print("Data saved as JSON files for each poet.")
