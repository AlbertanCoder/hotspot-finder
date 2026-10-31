"""Find hot spots in one thermal frame.

Pure logic: no files, no network, no camera. It takes numbers and returns
numbers, which is why it can be tested without any hardware.
"""


def find_hotspots(frame, threshold_c, min_pixels, width=32, height=24):
    """Group touching hot pixels into hotspots.

    frame is a flat list of temperatures, row by row, the same order the camera
    sends them. Pixel (x, y) lives at position y * width + x.

    Returns a list of dictionaries, one per hotspot:
      x, y    the centre of the hotspot (can fall between pixels, like 10.5)
      pixels  how many pixels it covers
      max_c   its hottest temperature
      cells   every (x, y) pixel in it, so the page can outline them
    """
    visited = [False] * (width * height)
    hotspots = []

    for y in range(height):
        for x in range(width):
            position = y * width + x
            if visited[position] or frame[position] <= threshold_c:
                continue
            # A hot pixel nobody has reached yet means a new hotspot starts here.
            cells = _flood_fill(frame, visited, x, y, threshold_c, width, height)
            if len(cells) >= min_pixels:
                hotspots.append(_summarize(frame, cells, width))

    return hotspots


def _flood_fill(frame, visited, start_x, start_y, threshold_c, width, height):
    """Collect every hot pixel connected to the starting pixel.

    Works like paint spreading from one pixel. to_check is a to-do list: take a
    pixel off it, keep it, and add its unvisited hot neighbours to the list.
    When the list is empty, the paint has reached every connected pixel.
    """
    visited[start_y * width + start_x] = True
    to_check = [(start_x, start_y)]
    cells = []

    while to_check:
        x, y = to_check.pop()
        cells.append((x, y))

        for next_x, next_y in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
            # Checking x and y, not list positions, stops the right edge of one
            # row from wrapping around to the left edge of the next row.
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue
            position = next_y * width + next_x
            if not visited[position] and frame[position] > threshold_c:
                # Mark it now, not when it is popped, so no pixel joins the
                # to-do list twice.
                visited[position] = True
                to_check.append((next_x, next_y))

    return cells


def _summarize(frame, cells, width):
    """Turn a list of pixels into the numbers the page needs."""
    return {
        "x": sum(x for x, _ in cells) / len(cells),
        "y": sum(y for _, y in cells) / len(cells),
        "pixels": len(cells),
        "max_c": max(frame[y * width + x] for x, y in cells),
        "cells": cells,
    }
