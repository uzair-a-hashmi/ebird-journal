import argparse

def log():
    print("log function triggered")

def history():
    print("history function triggered")

def lookup(species):
    print(f"lookup function triggered for {species}")

def nearby(location):
    print(f"nearby function location triggered for {location}")

parser = argparse.ArgumentParser(
    prog="eBird Journal",
    description="A personal birdwatching journal powered by eBird"
)

subparsers = parser.add_subparsers(required=True, help="Available commands")

# log command
parser_log = subparsers.add_parser("log", help="Log a new bird sighting")
parser_log.set_defaults(func=log)

# history command
parser_history = subparsers.add_parser("history", help="View your sighting history")
parser_history.set_defaults(func=history)

# lookup command
parser_lookup = subparsers.add_parser("lookup", help="Look up a species")
parser_lookup.add_argument("species", help="Species name to look up")
parser_lookup.set_defaults(func=lookup)

# nearby command
parser_nearby = subparsers.add_parser("nearby", help="Find recent sightings near a location")
parser_nearby.add_argument("location", help="Region code (e.g. US-NY)")
parser_nearby.set_defaults(func=nearby)

args = parser.parse_args()

if hasattr(args, "species"):
    args.func(args.species)
elif hasattr(args, "location"):
    args.func(args.location)
else:
    args.func()