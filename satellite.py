"""Download satellite hotspots from Canada's wildfire service and keep a copy.

The rule for this file: a bad download must never stop the program. The caller
always gets a list of points, plus a plain message if something went wrong.
"""
import csv
import os
import time
import urllib.request

import config


def get_points():
    """Return {"points": [{"lat": .., "lon": ..}, ..], "message": text or None}."""
    if _cache_is_fresh():
        return {"points": _read_points(), "message": None}

    try:
        _download()
        return {"points": _read_points(), "message": None}
    except Exception as problem:
        # Catching everything is deliberate: a dropped connection, a bad reply
        # and a full disk should all leave the demo running.
        reason = f"Satellite download failed: {problem}"

    if os.path.exists(config.SATELLITE_CACHE_FILE):
        return {"points": _read_points(), "message": reason + " Showing the last saved copy."}
    return {"points": [], "message": reason}


def _cache_is_fresh():
    if not os.path.exists(config.SATELLITE_CACHE_FILE):
        return False
    age_seconds = time.time() - os.path.getmtime(config.SATELLITE_CACHE_FILE)
    return age_seconds < config.SATELLITE_CACHE_SECONDS


def _download():
    with urllib.request.urlopen(config.SATELLITE_URL, timeout=config.SATELLITE_TIMEOUT_SECONDS) as reply:
        text = reply.read().decode("utf-8")

    # This service can answer "200 OK" with an error message in place of data.
    # Checking the header row stops that from being saved as good data.
    header = text.splitlines()[0].split(",") if text else []
    if "lat" not in header or "lon" not in header:
        raise ValueError("the reply had no lat and lon columns")

    # Write to a side file and swap it in, so a crash halfway through can never
    # leave a half-written cache behind.
    temporary_file = config.SATELLITE_CACHE_FILE + ".tmp"
    with open(temporary_file, "w", encoding="utf-8", newline="") as file:
        file.write(text)
    os.replace(temporary_file, config.SATELLITE_CACHE_FILE)


def _read_points():
    points = []
    with open(config.SATELLITE_CACHE_FILE, encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            try:
                points.append({"lat": float(row["lat"]), "lon": float(row["lon"])})
            except (KeyError, TypeError, ValueError):
                continue  # one damaged row should not lose all the others
    return points
