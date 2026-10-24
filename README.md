# eBird Journal

#### Description:

This is a journal I made that allows you to log birds you've seen and lookup bird sightings. It's a simple tool I made as my final project for Harvard's CS50P, which I took online. It's for birders like me who dislike context switching and just want to have an easy-to-access lookup tool to use in the terminal for looking up recent bird sightings.

## Features

- **log** - log a new bird sighting to your personal journal
- **history** - view your sighting history in a formatted table
- **lookup** - find recent sightings of a specific species in a country
- **nearby** - find recent sightings near any location in the world

## Installation

1. Clone the repository:

```
git clone https://github.com/uzair-a-hashmi/ebird-journal.git
cd ebird-journal
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Get a free eBird API key at ebird.org/api/keygen

4. Create a file called `config.py` in the project root with your API key:

```python
API_KEY = "your_ebird_api_key_here"
```

5. Run the program:

```
python project.py --help
```

## Usage

**log** - log a new bird sighting:

```
python project.py log
```

Prompts you for species name, location, date (leave blank for today), and optional notes. Saves to `journal.csv`.

**history** - view your sighting history:

```
python project.py history
```

Displays all logged sightings in a formatted table.

**lookup** - find recent sightings of a specific species:

```
python project.py lookup "American Robin"
python project.py lookup "Canada Goose" --region CA
```

Defaults to the US. Use `--region` with an ISO-2 country code to search elsewhere. Case insensitive - species name must match eBird's list of common names. Shows up to 10 results.

**nearby** - find recent sightings near a location:

```
python project.py nearby "Ithaca, NY"
python project.py nearby "Tokyo"
python project.py nearby "Paris, France"
```

Uses Nominatim to convert your search query to coordinates, then finds all recent sightings within 25km over the past 14 days. Shows up to 10 results. For best results, be specific with your search query.

## Configuration

This project requires a free eBird API key. Get one at ebird.org/api/keygen and add it to `config.py` as described in the Installation section. The `config.py` file is gitignored and will never be committed to the repository.

## Dependencies

- `requests` - HTTP requests to eBird and Nominatim APIs
- `tabulate` - formatted table output for history command
- `pycountry` - country code validation for lookup command

Location data provided by Nominatim/OpenStreetMap, used in accordance with their usage policy. Attribution: © OpenStreetMap contributors.

## Final Project for CS50P

This was built as the final project for Harvard's CS50P: Introduction to Programming with Python, completed independently online without formal enrollment.
