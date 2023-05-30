#!/usr/bin/env python

import fileinput
import subprocess
from argparse import ArgumentParser
from datetime import datetime
from typing import Optional

from AUR.RPC import AurRpc


__version__ = "0.1.0"

PRINT_OK = False

PackageNameSet = frozenset[str]


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()

    parser.add_argument("file", nargs="?", help="Defaults to stdin ('-')")
    parser.add_argument(
        "-o",
        "--orphans",
        action="store_true",
        help="ONLY list orphaned packages. Significantly faster as it skips getting package info from AUR RPC",
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)

    return parser


def list_out_of_date(package_names: PackageNameSet) -> PackageNameSet:
    # get info on package list from AUR RPC
    # this is to find packages that are marked out of date
    print("2. Getting out of date packages from AUR rpc")
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
    print("2. Finished listing out of date packages")

    hit_packages = frozenset(hit_packages)
    return hit_packages


def list_orphaned(package_names: PackageNameSet) -> PackageNameSet:
    print("1. Getting orphaned packages from AUR rpc")
    aur = AurRpc()
    orphaned_packages = aur.search("", by="maintainer")

    hit_packages = frozenset(p["Name"] for p in orphaned_packages)
    orphaned_packages = package_names.intersection(hit_packages)

    for package in orphaned_packages:
        print(f"Orphaned: {package}")
    print("1. Finished listing orphaned packages")

    return hit_packages


def list_nonexistent(
    package_names: PackageNameSet, existing_packages: PackageNameSet
) -> PackageNameSet:
    print("3. Calculating non-existent packages")
    nonexistent_packages = package_names.difference(existing_packages)

    for package in nonexistent_packages:
        print(f"Non-existent: {package}")
    print("3. Finished listing non-existent packages")
    return nonexistent_packages


def list_wiki_subprocess() -> PackageNameSet:
    print("Getting packages from script")
    stdout = subprocess.check_output("./list-wiki.sh", text=True)
    package_names = frozenset(stdout.splitlines())
    return package_names


def list_wiki_stdin(file: Optional[str] = None) -> PackageNameSet:
    if file is None:
        print("Reading packages from stdin")
    else:
        print(f"Reading packages from {file}")

    with fileinput.input(files=file) as lines:
        package_names = frozenset(li.strip() for li in lines)
    return package_names


def get_wiki_list(file: str) -> PackageNameSet:
    print("0. Getting list of packages to check")
    package_names = list_wiki_stdin(file)
    print(f"0. Arch wiki lists {len(package_names)} packages")
    return package_names


def main():
    parser = get_parser()
    args = parser.parse_args()

    # get a set of all AUR packages referenced in the Arch Wiki
    file: Optional[str] = args.file
    package_names = get_wiki_list(file)

    list_orphaned(package_names)
    only_list_orphans: bool = args.orphans
    if not only_list_orphans:
        existing_packages = list_out_of_date(package_names)
        list_nonexistent(
            package_names=package_names, existing_packages=existing_packages
        )


if __name__ == "__main__":
    main()
