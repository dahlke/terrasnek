#!/bin/bash

for i in test/*_test.py; do

echo "$i";

time python3 -m unittest $i

echo "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x";

done
