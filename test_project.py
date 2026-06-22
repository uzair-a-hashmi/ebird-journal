import os
import pytest
import csv
from datetime import date
from project import log, history, get_speciescode

def test_get_speciescode():
    assert get_speciescode("American Robin") == "amerob"
    assert get_speciescode("Canada Goose") == "cangoo"
    assert get_speciescode("common ostrich") == "ostric2"
    assert get_speciescode("PAINTED BUNTING") == "paibun"
    assert get_speciescode("not a real bird") == None


def test_log():
    if os.path.exists("journal.csv"):
        os.rename("journal.csv", "journal_backup.csv")
    
    try:
        with open("journal.csv", "w", newline="") as sightings:
            writer = csv.DictWriter(sightings, ["species name", "location of sighting", "date seen", "notes (optional)"])
            writer.writeheader()
        
        log("Red Cardinal", "Ithaca, NY", "2026-06-20", "Some notes here")
        log("Painted Bunting", "Dallas, TX", "", "")
        log("American Robin", "Princeton, NJ", "2019-07-12", "Hello World")
        
        with open("journal.csv", newline="") as sightings:
            reader = csv.DictReader(sightings)
            rows = list(reader)
            assert rows[0]["species name"] == "Red Cardinal"
            assert rows[0]["location of sighting"] == "Ithaca, NY"
            assert rows[0]["date seen"] == "2026-06-20"
            assert rows[0]["notes (optional)"] == "Some notes here"
            assert rows[1]["species name"] == "Painted Bunting"
            assert rows[1]["date seen"] == str(date.today())
            assert rows[1]["notes (optional)"] == "None"
            assert rows[2]["species name"] == "American Robin"
            assert rows[2]["date seen"] == "2019-07-12"
            assert rows[2]["notes (optional)"] == "Hello World"
    finally:
        os.remove("journal.csv")
        if os.path.exists("journal_backup.csv"):
            os.rename("journal_backup.csv", "journal.csv")


def test_history():
    if os.path.exists("journal.csv"):
        os.rename("journal.csv", "journal_backup.csv")
    
    try:
        # create fresh journal with known data
        with open("journal.csv", "w", newline="") as sightings:
            writer = csv.DictWriter(sightings, ["species name", "location of sighting", "date seen", "notes (optional)"])
            writer.writeheader()
        
        log("Red Cardinal", "Ithaca, NY", "2026-06-20", "Some notes here")
        log("American Robin", "Princeton, NJ", "2019-07-12", "Hello World")
        
        result = history()
        
        assert "Red Cardinal" in result
        assert "Ithaca, NY" in result
        assert "American Robin" in result
        assert "Princeton, NJ" in result
        assert "2026-06-20" in result
        assert "Hello World" in result
    finally:
        os.remove("journal.csv")
        if os.path.exists("journal_backup.csv"):
            os.rename("journal_backup.csv", "journal.csv")