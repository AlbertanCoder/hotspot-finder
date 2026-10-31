# Night Hotspot Finder

A prototype of the software side of night hotspot mapping: a low-cost thermal camera plus AI that finds hot spots in the dark and turns them into map coordinates and a short briefing for a wildfire ground crew.

**This is a learning prototype. It is not a certified system and must not be used for real wildfire decisions.**

Work in progress. Right now it runs on fake camera data and shows real satellite hotspots from the Canadian Wildland Fire Information System.

## How to run it (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

Then open http://127.0.0.1:5000

## How to test it

```powershell
.venv\Scripts\python.exe -m pytest
```
