"""Every setting for the project, in one place, so nothing is buried in the code."""

# Where frames come from: "fake" for now. "serial" and "replay" arrive in Step 3.
MODE = "fake"
SERIAL_PORT = "COM5"
REPLAY_FILE = "recordings/demo.csv"

# A pixel hotter than this counts as hot. 35 C sits above a cool room and warm
# ground, but well below the 40-80 C blobs we want to catch.
THRESHOLD_C = 35.0
# Raise this to ignore tiny specks. 1 means a single hot pixel counts.
MIN_PIXELS = 1

# The point the camera looks down on, near Slave Lake, Alberta.
CAMERA_LAT = 55.28
CAMERA_LON = -114.77

# The demo pretends the camera is on a drone this high, looking straight down.
PRETEND_ALTITUDE_M = 120
FOV_X_DEG = 55
FOV_Y_DEG = 35

CLAUDE_MODEL = "claude-haiku-5-5"

# Canada's wildfire service: satellite hotspots from the last 24 hours, as CSV.
# propertyName keeps only lat and lon, which cuts the download from about 720 KB
# to about 120 KB. The older hotspots.csv address now returns 404.
SATELLITE_URL = (
    "https://cwfis.cfs.nrcan.gc.ca/geoserver/public/ows"
    "?service=WFS&version=2.0.0&request=GetFeature"
    "&typeNames=public:hotspots_last24hrs&outputFormat=csv"
    "&propertyName=lat,lon"
)
SATELLITE_CACHE_FILE = "satellite_cache.csv"
SATELLITE_CACHE_SECONDS = 3600  # 1 hour: satellites pass a few times a day
SATELLITE_TIMEOUT_SECONDS = 20
