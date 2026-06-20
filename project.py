import argparse
import csv
import requests
import json
from os import path
from datetime import date as dt
from tabulate import tabulate

def log(species, location, date, notes):
    if not date:
        date = dt.today()
    if not notes:
        notes = "None"
    
    with open("journal.csv", "a", newline="") as sightings:
        writer = csv.DictWriter(sightings, ["species name", "location of sighting", "date seen", "notes (optional)"])
        writer.writerow({"species name": species, "location of sighting": location, "date seen": date, "notes (optional)": notes})


def history():
    with open("journal.csv") as journal:
        reader = csv.DictReader(journal)
        return tabulate(reader, headers="keys", tablefmt="fancy_grid")

def get_speciescode(common_name):
    response = requests.get("https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json")
    specieslist = response.json()
    for species in specieslist:
        if common_name == species["comName"]:
            return species["speciesCode"]
    return


def lookup(species, regioncode):
    speciescode = get_speciescode(species)
    if not speciescode:
        return
    api_key = "oalab1htmiag"
    response = requests.get(f"https://api.ebird.org/v2/data/obs/{regioncode}/recent/{speciescode}?maxResults=10", headers={"x-ebirdapitoken": api_key})
    observations = response.json()
    for observation in observations:
        yield f"⚝ Sighting! {observation["locName"]} at {observation["obsDt"]}"
    
def nearby(location):
    print(f"nearby function location triggered for {location}")

def main():
    parser = argparse.ArgumentParser(
        prog="eBird Journal",
        description="A personal birdwatching journal powered by eBird"
    )

    subparsers = parser.add_subparsers(required=True, help="Available commands")

    # log command
    parser_log = subparsers.add_parser("log", help="Log a new bird sighting")
    parser_log.set_defaults(command="log")

    # history command
    parser_history = subparsers.add_parser("history", help="View your sighting history")
    parser_history.set_defaults(command="history")

    # lookup command
    parser_lookup = subparsers.add_parser("lookup", help="Look up a species")
    parser_lookup.add_argument("species", help="Species name to look up")
    parser_lookup.add_argument("--region", help="region code e.g. GB, FR, JP (default: US)", default="US")
    parser_lookup.set_defaults(command="lookup")

    # nearby command
    parser_nearby = subparsers.add_parser("nearby", help="Find recent sightings near a location")
    parser_nearby.add_argument("location", help="Region code (e.g. US-NY)")
    parser_nearby.set_defaults(command="nearby")

    args = parser.parse_args()

    match args.command:
        case "log":
            # create journal.csv if it doesn't already exist, and add header
            if not path.exists("journal.csv"):
                with open("journal.csv", "w", newline="") as sightings:
                    writer = csv.DictWriter(sightings, ["species name", "location of sighting", "date seen", "notes (optional)"])
                    writer.writeheader()
            
            # while loop to add rows
            while True:
                # while loop to check if species isn't empty
                while True:
                    if species := input("Enter species name: "):
                        break

                # while loop to check if location isn't empty
                while True:
                    if location := input("Enter location: "):
                        break
                
                # while loop to check if date is valid format (YYYY-MM-DD)
                while True:
                    if date := input("Enter date, format YYYY-MM-DD (leave blank if today): "):
                        try:
                            # makes sure format looks like [...]-[...]-[...]
                            year, month, day = date.split("-")

                            # makes sure format looks like [integer]-[integer]-[integer] 
                            # and integers are in the correct range for year, month, day
                            date = dt(int(year), int(month), int(day))

                            difference = date - dt.today()
                        except ValueError:
                            pass
                        else:
                            # makes sure correct number of digits for year, month, and day
                            # and date is not in the future
                            if len(year) == 4 and len(month) == 2 and len(day) == 2 and difference.days <= 0:
                                break
                    else:
                        break
                
                # no check needed for notes
                notes = input("Enter notes (leave blank if none): ")

                log(species, location, date, notes)

                print("Sighting logged successfully!", end=" ")

                # while loop to make sure user types either y or n to continue
                while True:
                    choice = input("Log another sighting? (Y/N) ")

                    if choice.lower() == "n":
                        return
                    elif choice.lower() == "y":
                        break
        case "history":
            if path.exists("journal.csv"):
                print(history())
            else:
                print("Your journal doesn't exist yet! Create one with the log command.")
        case "lookup":
            for sighting in lookup(args.species, args.region):
                print(sighting)

if __name__ == "__main__":
    main()