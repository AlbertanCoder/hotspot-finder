"""All settings for the hotspot finder live in this one file.

Why one file: on demo day, if something looks wrong, this is the first place
to check. Nothing else in the project should hard-code a number.
"""

# How we get frames: "fake" (made up), "serial" (real camera), "replay" (recording).
MODE = "fake"

# Serial port the QT Py shows up on (used from Step 3).
# Find yours with: python app.py --list-ports
SERIAL_PORT = "COM5"

# A pixel counts as hot when it is ABOVE this temperature (degrees Celsius).
# Strictly above: a pixel exactly at THRESHOLD_C is not a hotspot.
THRESHOLD_C = 35.0

# Ignore hotspots smaller than this many pixels (1 = keep everything).
MIN_PIXELS = 1

# The ground point the camera looks straight down on.
# Default: a spot near Slave Lake, Alberta.
CAMERA_LAT = 55.28
CAMERA_LON = -114.77

# The demo pretends the camera hangs on a drone this high (metres),
# pointing straight down.
PRETEND_ALTITUDE_M = 120.0

# Camera lens field of view in degrees (Adafruit 55 degree lens, part 4407):
# 32 columns x 24 rows of pixels.
FOV_X_DEG = 55.0
FOV_Y_DEG = 35.0

# Satellite hotspots farther than this from the camera point are hidden.
# 500 km = "northern Alberta and BC": our region, not all of North America.
SATELLITE_RADIUS_KM = 500.0

# Recording to play back in replay mode (used from Step 3).
REPLAY_FILE = ""

# Claude model that writes the morning briefing (used from Step 5).
CLAUDE_MODEL = "claude-haiku-5-5"
