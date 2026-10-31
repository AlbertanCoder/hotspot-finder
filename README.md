# Night Hotspot Finder

A low-cost thermal camera plus AI that finds hot spots in the dark and turns
them into map coordinates and a short morning briefing for a wildfire ground
crew. It is a prototype of the software side of night hotspot mapping — the
work Alberta Wildfire hires drone crews for.

**This is a student demo prototype, not a certified system.** It is not
approved for wildfire operations or public safety decisions. Professional
crews already do this work with certified equipment and trained staff.

## Status

Step 1 of 6 is done: fake thermal frames, hotspot detection, the CWFIS
satellite layer, and the map page. The real camera, map coordinates for
detected hotspots, and the AI briefing arrive in later steps.

## How to run (Step 1 — no hardware needed)

```powershell
cd C:\Users\SHADHUNTER\hotspot-finder
python -m venv .venv                                                     # first time only
.\.venv\Scripts\python.exe -m pip install flask pyserial pytest         # first time only
.\.venv\Scripts\python.exe app.py
```

Then open http://127.0.0.1:5000 in a browser. The left side shows the fake
thermal picture with detected hot spots outlined in white; the right side
shows real satellite hotspots near the camera point as orange dots.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Sources

- Satellite hotspots: CWFIS (Canadian Wildland Fire Information System),
  Natural Resources Canada — https://cwfis.cfs.nrcan.gc.ca
  (daily files under /downloads/hotspots/; contains information licensed
  under the Open Government Licence — Canada)
- Map: Leaflet + OpenStreetMap tiles — https://leafletjs.com
- Thermal camera: Adafruit MLX90640 guide —
  https://learn.adafruit.com/adafruit-mlx90640-ir-thermal-camera

## Honest limits

- Resolution is low: 32 x 24 pixels, so a "hotspot" is a blob several metres
  wide, not an exact fire location.
- The camera position is approximate: the demo pretends the camera hangs on
  a drone at a fixed spot looking straight down.
- The MLX90640 is about ±2 °C accurate between 0 and 100 °C.
- Tests so far are handheld on a bench, not flown on a drone.
- **Not certified for operations.** Professional crews already do this work
  with certified equipment; this is a learning project and a demo.
