#!/bin/bash

cat ./all_poems.txt | grep -vE "^[۰١٢٣٤٥٦٧٨٩12 34\.567890٠١٢\t \(\)٣٤٥٦٧٨٩]+$" | grep -vE "^$" | grep -vE "^[ــ \t \n ــــ**٭•+\-\=]+$" >cleaned.txt
