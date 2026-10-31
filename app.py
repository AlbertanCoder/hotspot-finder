"""The web server: hands the page its files and its live data."""
from flask import Flask, jsonify

import config
import hotspots
import satellite
import sources

app = Flask(__name__, static_folder="static", static_url_path="")
camera = sources.make_camera(config.MODE)


@app.get("/")
def home():
    return app.send_static_file("index.html")


@app.get("/api/state")
def state():
    """One fresh frame and the hotspots found in it. The page asks twice a second."""
    frame = camera.read()
    found = hotspots.find_hotspots(frame, config.THRESHOLD_C, config.MIN_PIXELS)
    return jsonify(
        mode=config.MODE,
        width=sources.WIDTH,
        height=sources.HEIGHT,
        frame=frame,
        hotspots=found,
    )


@app.get("/api/satellite")
def satellite_points():
    """Separate from /api/state so a slow download can't freeze the heat image."""
    return jsonify(satellite.get_points())


@app.get("/api/config")
def page_config():
    """Settings the page needs once, when it first loads."""
    return jsonify(camera_lat=config.CAMERA_LAT, camera_lon=config.CAMERA_LON)


if __name__ == "__main__":
    # 127.0.0.1 keeps the server on this laptop, away from any shared Wi-Fi.
    app.run(host="127.0.0.1", port=5000)
