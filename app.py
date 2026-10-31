"""Flask server: serves the map page and the /api/state JSON endpoint.

Run it with:  python app.py   then open http://127.0.0.1:5000
"""

from flask import Flask, jsonify, send_from_directory

import config
import hotspots
import satellite
import sources

app = Flask(__name__, static_folder="static", static_url_path="")

# One camera object for the whole run; config.MODE decides which one.
# Step 1 has only the fake camera (serial and replay come in Step 3).
if config.MODE == "fake":
    camera = sources.FakeCamera()
else:
    raise RuntimeError("Step 1 only supports MODE = 'fake'; serial/replay come in Step 3")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/state")
def api_state():
    """One JSON snapshot: the frame, the hotspots found in it, and satellite data."""
    frame = camera.read_frame()
    return jsonify(
        mode=config.MODE,
        width=camera.width,
        height=camera.height,
        threshold_c=config.THRESHOLD_C,
        frame=frame,
        hotspots=hotspots.find_hotspots(
            frame,
            width=camera.width,
            height=camera.height,
            threshold_c=config.THRESHOLD_C,
            min_pixels=config.MIN_PIXELS,
        ),
        camera={"lat": config.CAMERA_LAT, "lon": config.CAMERA_LON},
        satellite=satellite.get_satellite_hotspots(),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
