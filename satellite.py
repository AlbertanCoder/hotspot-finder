"""Download and cache CWFIS satellite hotspots (fires seen from space).

CWFIS = Canadian Wildland Fire Information System (Natural Resources Canada).
It publishes one CSV per day of satellite-detected hotspots for North America,
named YYYYMMDD.csv under https://cwfis.cfs.nrcan.gc.ca/downloads/hotspots/

NOTE: the old single file "hotspots.csv" no longer exists on the server; this
module was written against the real files found there (columns: lat, lon,
rep_date, source, sensor, ...).
"""

import csv
import datetime
import io
import math
import os
import time
import urllib.error
import urllib.request

import config

BASE_URL = "https://cwfis.cfs.nrcan.gc.ca/downloads/hotspots/"
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "hotspots.csv")
CACHE_MAX_AGE_S = 60 * 60  # keep a downloaded copy for 1 hour


def get_satellite_hotspots():
    """Return {"points": [...], "total": n, "radius_km": k, "error": None|str}.

    Each point is {"lat": ..., "lon": ..., "rep_date": ...}, and only points
    within SATELLITE_RADIUS_KM of the camera point are included.

    This function never raises: any failure comes back as a clear error
    string so the page can show a message and keep running.
    """
    try:
        raw, warning = _load_csv()
    except Exception as exc:
        return {"points": [], "total": 0, "radius_km": config.SATELLITE_RADIUS_KM,
                "error": "satellite data unavailable: %s" % exc}
    try:
        points, total = _parse_and_filter(raw)
    except Exception as exc:
        return {"points": [], "total": 0, "radius_km": config.SATELLITE_RADIUS_KM,
                "error": "satellite file not understood: %s" % exc}
    return {"points": points, "total": total,
            "radius_km": config.SATELLITE_RADIUS_KM, "error": warning}


def _load_csv():
    """Return (csv_text, warning). Downloads only when the cache is old/missing."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    if os.path.exists(CACHE_FILE):
        age = time.time() - os.path.getmtime(CACHE_FILE)
        if age < CACHE_MAX_AGE_S:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return f.read(), None
    try:
        text = _download()
    except Exception as exc:
        # Download failed. An old copy beats no copy; the page is told so.
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return f.read(), "using cached satellite data (download failed: %s)" % exc
        raise
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    return text, None


def _download():
    """Fetch today's hotspot file, falling back to yesterday's if needed."""
    today = datetime.date.today()
    last_error = None
    for days_back in (0, 1):
        day = today - datetime.timedelta(days=days_back)
        url = BASE_URL + day.strftime("%Y%m%d") + ".csv"
        req = urllib.request.Request(url, headers={"User-Agent": "hotspot-finder-demo"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            last_error = "%s gave HTTP %s" % (url, exc.code)
            if exc.code != 404:
                raise  # a real problem: do not hide it behind a fallback
    raise RuntimeError(last_error)


def _parse_and_filter(raw):
    """Return (points_near_camera, total_rows_in_file)."""
    reader = csv.DictReader(io.StringIO(raw))
    points = []
    total = 0
    for row in reader:
        total += 1
        lat = float(row["lat"])
        lon = float(row["lon"])
        if _km_between(config.CAMERA_LAT, config.CAMERA_LON, lat, lon) <= config.SATELLITE_RADIUS_KM:
            points.append({"lat": lat, "lon": lon, "rep_date": row.get("rep_date", "")})
    return points, total


def _km_between(lat1, lon1, lat2, lon2):
    """Great-circle distance between two points on Earth, in km (haversine)."""
    r = 6371.0  # Earth radius in km; good enough for a distance filter
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))
