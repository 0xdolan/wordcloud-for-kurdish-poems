#!/bin/bash

# Define input and output files
input_file="./allekok/all_poems_concatenated.txt"
output_file="./allekok/all_poems_concatenated_cleaned.txt"

# Filter lines based on above specified patterns and write to output file
grep -Ev "^[۰١٢٣٤٥٦٧٨٩12 34\.567890٠١٢\t \(\)٣٤٥٦٧٨٩]+$|^$|^[ــ \t \n ــــ**٭•+\-\=]+$" "$input_file" >"$output_file"
