#!/usr/bin/env python

import subprocess


def main():
    # get a set of all AUR packages referenced in the Arch Wiki
    stdout = subprocess.check_output("./list-wiki.sh", text=True)
    package_names = frozenset(stdout.splitlines())
    print(package_names)


if __name__ == "__main__":
    main()
