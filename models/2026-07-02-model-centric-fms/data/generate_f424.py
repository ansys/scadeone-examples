"""
Generate the ``f-424`` navigation database used by the FMS model.

The file is a simplified, fixed-width, ARINC 424-like text file built from the
public-domain OurAirports open data (https://ourairports.com/data/).
It is NOT a certified ARINC 424 database and must not be used for navigation.
"""

import csv
from math import atan2, cos, degrees, radians, sin
from pathlib import Path
from typing import TextIO
import unicodedata
import urllib.request

# Configuration
DATA_URL = "https://davidmegginson.github.io/ourairports-data/"
CSV_FILES = ["airports.csv", "runways.csv"]
AIRPORTS_CSV = Path("airports.csv")
RUNWAYS_CSV = Path("runways.csv")
OUTPUT_FILE = Path("f-424")


def download_data() -> None:
    """Download airport and runway data from OurAirports."""
    print("Downloading data files...")
    for fname in CSV_FILES:
        print(f"  Downloading {fname}...")
        urllib.request.urlretrieve(DATA_URL + fname, fname)
    print("All files downloaded")


def remove_accents(text: str) -> str:
    """Remove accents from text and convert to ASCII."""
    normalized = unicodedata.normalize("NFD", text)
    ascii_text = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )
    return ascii_text.encode("ascii", "replace").decode("ascii")


def format_lat(lat: float) -> str:
    """Return latitude in DDMMSSN/S format."""
    deg = int(abs(lat))
    minutes = int((abs(lat) - deg) * 60)
    seconds = int(((abs(lat) * 60) - (deg * 60) - minutes) * 60)
    hemi = "N" if lat >= 0 else "S"
    return f"{deg:02d}{minutes:02d}{seconds:02d}{hemi}"


def format_lon(lon: float) -> str:
    """Return longitude in DDDMMSSW/E format."""
    deg = int(abs(lon))
    minutes = int((abs(lon) - deg) * 60)
    seconds = int(((abs(lon) * 60) - (deg * 60) - minutes) * 60)
    hemi = "E" if lon >= 0 else "W"
    return f"{deg:03d}{minutes:02d}{seconds:02d}{hemi}"


def format_elevation(elev_ft: str) -> str:
    """Return elevation as +XXXXX (5 digits, signed)."""
    try:
        elev = int(float(elev_ft))
    except (ValueError, TypeError):
        elev = 0
    sign = "+" if elev >= 0 else "-"
    return f"{sign}{abs(elev):05d}"


def normalize_surface(surface: str) -> str:
    """Normalize runway surface type to 8-character string."""
    if not surface or not surface.strip():
        return "UNKNOWN "
    s = surface.strip().lower()

    # Asphalt
    if (
        "asph" in s
        or "asphalt" in s
        or "ashp" in s
        or "bitumen" in s
        or "blacktop" in s
        or "macadam" in s
        or "tar" in s
        or "asp" in s
    ):
        if "concrete" in s or "conc" in s:
            return "ASPHALTC"
        return "ASPHALT "
    # Concrete
    if (
        "conc" in s
        or "concrete" in s
        or "cement" in s
        or "cemen" in s
        or "ccn" in s
        or "con" in s
    ):
        return "CONCRETE"
    # Grass
    if "grass" in s or "turf" in s or "sod" in s or "herbe" in s or "gras" in s:
        return "GRASS   "
    # Gravel
    if (
        "gravel" in s
        or "grvl" in s
        or "grv" in s
        or "coral" in s
        or "crushed rock" in s
        or "shale" in s
        or "murram" in s
        or "maicillo" in s
    ):
        return "GRAVEL  "
    # Dirt/Earth/Clay/Loam
    if (
        "dirt" in s
        or "earth" in s
        or "clay" in s
        or "loam" in s
        or "soil" in s
        or "ground" in s
        or "eartth" in s
        or "eerth" in s
    ):
        return "DIRT    "
    # Sand
    if "sand" in s or "piçarra" in s or "laterite" in s:
        return "SAND    "
    # Snow/Ice
    if "snow" in s or "ice" in s:
        return "SNOW    "
    # Water
    if "water" in s or "wate" in s or "summer water" in s:
        return "WATER   "
    return "UNKNOWN "


def compute_heading(lat1: str, lon1: str, lat2: str, lon2: str) -> float:
    """Compute heading between two points."""
    lat1_f, lon1_f, lat2_f, lon2_f = map(float, [lat1, lon1, lat2, lon2])
    dlon = radians(lon2_f - lon1_f)
    lat1_rad = radians(lat1_f)
    lat2_rad = radians(lat2_f)
    x = sin(dlon) * cos(lat2_rad)
    y = cos(lat1_rad) * sin(lat2_rad) - sin(lat1_rad) * cos(lat2_rad) * cos(dlon)
    initial_heading = atan2(x, y)
    heading_deg = (degrees(initial_heading) + 360) % 360
    return round(heading_deg, 1)


def generate_airports(out: TextIO) -> int:
    """Generate airport records and write to output file."""
    print("Processing airports...")
    count = 0

    with AIRPORTS_CSV.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            icao = (row.get("icao_code") or "").strip().upper()
            if not icao:
                continue  # skip if no ICAO code

            name = remove_accents((row.get("name") or "").upper())
            lat = float(row["latitude_deg"])
            lon = float(row["longitude_deg"])
            elev = row.get("elevation_ft", "0")

            # pad name to 32 chars
            name_padded = (name[:32]).ljust(32)

            line = (
                f"AP{icao}{name_padded}"
                f"{format_lat(lat)}  "
                f"{format_lon(lon)}  "
                f"{format_elevation(elev)}"
            )

            out.write(line + "\n")
            count += 1

    print(f"{count} airport records processed")
    return count


def generate_runways(out: TextIO) -> int:
    """Generate runway records and write to output file."""
    print("Processing runways...")
    count = 0

    with RUNWAYS_CSV.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            icao = (row.get("airport_ident") or "").strip().upper()
            if not icao or len(icao) != 4:
                continue

            if row.get("closed", "").strip().lower() == "true":
                continue

            # Check required fields
            if not all(
                [
                    row.get("le_latitude_deg"),
                    row.get("le_longitude_deg"),
                    row.get("he_latitude_deg"),
                    row.get("he_longitude_deg"),
                    row.get("length_ft"),
                    row.get("width_ft"),
                ]
            ):
                continue

            surface = row.get("surface", "UNKNOWN")

            # Generate headings
            le_heading = compute_heading(
                row["le_latitude_deg"],
                row["le_longitude_deg"],
                row["he_latitude_deg"],
                row["he_longitude_deg"],
            )
            he_heading = compute_heading(
                row["he_latitude_deg"],
                row["he_longitude_deg"],
                row["le_latitude_deg"],
                row["le_longitude_deg"],
            )

            # Write both runway ends
            for end_data in [
                (
                    row["le_ident"],
                    row["le_latitude_deg"],
                    row["le_longitude_deg"],
                    row["le_elevation_ft"],
                    le_heading,
                ),
                (
                    row["he_ident"],
                    row["he_latitude_deg"],
                    row["he_longitude_deg"],
                    row["he_elevation_ft"],
                    he_heading,
                ),
            ]:
                ident, lat, lon, elev, heading = end_data

                if not ident or not lat or not lon:
                    continue

                ident = ident.strip().upper()
                surface_str = normalize_surface(surface).ljust(8)
                heading_str = f"{int(heading * 10):04d}"

                line = (
                    f"RW{icao}{ident:4s}"
                    f"{format_lat(float(lat))}  "
                    f"{format_lon(float(lon))}  "
                    f"{format_elevation(elev)} "
                    f"{int(float(row['length_ft'])):05d}"
                    f"{int(float(row['width_ft'])):03d}"
                    f"{surface_str}{heading_str}"
                )

                out.write(line + "\n")
                count += 1

    print(f"{count} runway records processed")
    return count


def main() -> None:
    """Download the source data and write the f-424 file."""
    print("Starting f-424 file generation...")

    # Step 1: Download data
    download_data()

    # Step 2: Generate consolidated file
    print(f"Generating consolidated file: {OUTPUT_FILE}")

    with OUTPUT_FILE.open("w", encoding="ascii", errors="replace") as out:
        airport_count = generate_airports(out)
        runway_count = generate_runways(out)

    total_count = airport_count + runway_count
    print(f"Complete: {total_count} records written to {OUTPUT_FILE}")
    print(f"   - {airport_count} airports")
    print(f"   - {runway_count} runways")


if __name__ == "__main__":
    main()
