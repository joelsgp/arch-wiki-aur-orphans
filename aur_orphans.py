#!/usr/bin/env python

import fileinput
import subprocess
from argparse import ArgumentParser
from datetime import datetime
from typing import Optional

from AUR.RPC import AurRpc


PRINT_OK = False


PackageNames = frozenset[str]


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("file", nargs="?")
    return parser


def list_out_of_date(package_names: PackageNames) -> PackageNames:
    # get info on package list from AUR RPC
    # this is to find packages that are marked out of date
    print("Getting out of date packages from AUR rpc")
    aur = AurRpc()
    package_info = aur.info(package_names)

    # this is for finding which packages are nonexistent
    hit_packages = set()

    for package in package_info:
        name = package["Name"]
        hit_packages.add(name)
        out_of_date = package["OutOfDate"]
        if out_of_date is not None:
            timestamp = datetime.utcfromtimestamp(out_of_date)
            time_formatted = timestamp.isoformat()
            print(f"Out of date ({time_formatted}): {name}")
        else:
            if PRINT_OK:
                print(f"OK: {name}")
    print("Finished listing out of date packages")

    hit_packages = frozenset(hit_packages)
    return hit_packages


def list_orphaned(package_names: PackageNames) -> PackageNames:
    print("Getting orphaned packages from AUR rpc")
    aur = AurRpc()
    orphaned_packages = aur.search("", by="maintainer")

    hit_packages = frozenset(p["Name"] for p in orphaned_packages)
    orphaned_packages = package_names.intersection(hit_packages)

    for package in orphaned_packages:
        print(f"Orphaned: {package}")
    print("Finished listing orphaned packages")

    return hit_packages


def list_wiki_subprocess() -> PackageNames:
    print("Getting packages from script")
    stdout = subprocess.check_output("./list-wiki.sh", text=True)
    package_names = frozenset(stdout.splitlines())
    return package_names


def list_wiki_stdin(file: Optional[str] = None) -> PackageNames:
    if file is None:
        print("Reading packages from stdin")
    else:
        print(f"Reading packages from {file}")

    with fileinput.input(files=file) as lines:
        package_names = frozenset(lines)
    return package_names


def main():
    parser = get_parser()
    args = parser.parse_args()
    file: Optional[str] = args.file

    # get a set of all AUR packages referenced in the Arch Wiki
    print("Getting list of packages to check")
    package_names = list_wiki_stdin(file)
    print(f"Arch wiki lists {len(package_names)} packages")

    # list_out_of_date(package_names)
    list_orphaned(package_names)


if __name__ == "__main__":
    main()
