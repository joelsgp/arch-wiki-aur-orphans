#!/bin/bash
set -eux
./list-wiki.sh > packages.txt
cat packages.txt | ./aur_orphans.py
