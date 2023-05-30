#!/bin/bash
set -eux
grep --recursive --only-matching --no-filename --perl-regexp \
    --regexp='(?<=https://aur.archlinux.org/packages/)[a-z0-9@\._+\-]+(?=/)' \
    '/usr/share/doc/arch-wiki/html/'
