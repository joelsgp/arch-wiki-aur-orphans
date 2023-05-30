#!/usr/bin/env python

import subprocess
from datetime import datetime

from AUR.RPC import AurRpc


PRINT_OK = False


PackageNames = frozenset[str]


def list_out_of_date(package_names: PackageNames) -> PackageNames:
    # get info on package list from AUR RPC
    # this is to find packages that are marked out of date
    print("Getting package info from AUR rpc")
    aur = AurRpc()
    package_info = aur.info(package_names)

    # this is for finding which packages are nonexistent
    hit_packages = set()

    print("Checking out of date packages")
    for package in package_info:
        name = package["Name"]
        hit_packages.add(name)
        out_of_date = package["OutOfDate"]
        if out_of_date is not None:
            timestamp = datetime.utcfromtimestamp(out_of_date)
            time_formatted = timestamp.isoformat()
            print(f"Out of date: {name}, {time_formatted}")
        else:
            if PRINT_OK:
                print(f"OK: {name}")

    hit_packages = frozenset(hit_packages)
    return hit_packages


def main():
    # get a set of all AUR packages referenced in the Arch Wiki
    print("Getting list of packages to check")
    stdout = subprocess.check_output("./list-wiki.sh", text=True)
    package_names = frozenset(stdout.splitlines())
    print(f"Arch wiki lists {len(package_names)} packages")

    list_out_of_date(package_names)

    # print("Getting orphaned packages from AUR rpc")


if __name__ == "__main__":
    main()
