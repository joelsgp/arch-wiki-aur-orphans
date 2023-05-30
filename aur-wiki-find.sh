#!/bin/bash
set -eux
grep --recursive --only-matching --perl-regexp \
    --regexp="(?<=https://aur.archlinux.org/packages/)${1}(?=/)" \
    '/usr/share/doc/arch-wiki/html/'
