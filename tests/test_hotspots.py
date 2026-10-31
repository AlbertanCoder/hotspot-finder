"""Tests for hotspots.py.

A frame is a flat list of 768 temperatures (24 rows x 32 columns, row by row),
so the pixel at (x, y) lives at index y * 32 + x.
"""

import hotspots

W, H = 32, 24


def make_frame(fill=18.0):
    """A boring frame: every pixel at `fill` degrees."""
    return [fill] * (W * H)


def set_pixel(frame, x, y, temp):
    frame[y * W + x] = temp


def test_no_hotspot_all_normal():
    frame = make_frame(18.0)
    assert hotspots.find_hotspots(frame, threshold_c=35.0, min_pixels=1) == []


def test_no_hotspot_when_all_just_below_threshold():
    frame = make_frame(34.9)
    assert hotspots.find_hotspots(frame, threshold_c=35.0, min_pixels=1) == []


def test_one_blob():
    frame = make_frame()
    for x in range(5, 8):
        for y in range(5, 8):
            set_pixel(frame, x, y, 50.0)   # a 3x3 square blob
    set_pixel(frame, 6, 6, 55.0)           # hottest pixel in the middle
    hs = hotspots.find_hotspots(frame, threshold_c=35.0, min_pixels=1)
    assert len(hs) == 1
    h = hs[0]
    assert h["pixels"] == 9                # record: "pixels" = pixel count
    assert h["max_c"] == 55.0
    assert (h["x"], h["y"]) == (6, 6)      # centre of the 3x3 square


def test_two_separate_blobs():
    frame = make_frame()
    set_pixel(frame, 3, 3, 45.0)           # one lone hot pixel
    set_pixel(frame, 20, 10, 60.0)         # another, far away
    hs = hotspots.find_hotspots(frame, threshold_c=35.0, min_pixels=1)
    assert len(hs) == 2
    assert hs[0]["max_c"] == 60.0          # sorted hottest first
    assert (hs[0]["x"], hs[0]["y"]) == (20, 10)
    assert hs[1]["max_c"] == 45.0
    assert (hs[1]["x"], hs[1]["y"]) == (3, 3)


def test_blob_touching_the_edge():
    frame = make_frame()
    for y in range(0, 3):
        set_pixel(frame, 0, y, 50.0)       # 3 pixels down the left edge
    hs = hotspots.find_hotspots(frame, threshold_c=35.0, min_pixels=1)
    assert len(hs) == 1
    assert hs[0]["pixels"] == 3
    assert hs[0]["x"] == 0
    assert hs[0]["y"] == 1


def test_threshold_exactly_equal():
    # A pixel exactly AT the threshold is NOT "above" it -> not a hotspot.
    frame = make_frame()
    set_pixel(frame, 10, 10, 35.0)         # exactly at threshold: ignored
    set_pixel(frame, 11, 10, 35.1)         # just above threshold: hot
    hs = hotspots.find_hotspots(frame, threshold_c=35.0, min_pixels=1)
    assert len(hs) == 1
    assert (hs[0]["x"], hs[0]["y"]) == (11, 10)
    assert hs[0]["pixels"] == 1


def test_centre_rounding_on_even_sized_blob():
    # 2x2 blob: the mean x is 10.5 and the mean y is 10.5. Python's round()
    # breaks ties toward the even number, so the centre is (10, 10).
    frame = make_frame()
    for x in (10, 11):
        for y in (10, 11):
            set_pixel(frame, x, y, 50.0)
    hs = hotspots.find_hotspots(frame, threshold_c=35.0, min_pixels=1)
    assert len(hs) == 1
    assert (hs[0]["x"], hs[0]["y"]) == (10, 10)
    assert hs[0]["pixels"] == 4


def test_min_pixels_drops_small_blobs():
    frame = make_frame()
    set_pixel(frame, 2, 2, 50.0)           # 1-pixel blob: too small
    for x in range(10, 12):
        set_pixel(frame, x, 5, 50.0)       # 2-pixel blob: kept
    hs = hotspots.find_hotspots(frame, threshold_c=35.0, min_pixels=2)
    assert len(hs) == 1
    assert hs[0]["pixels"] == 2


def test_diagonal_pixels_are_not_one_hotspot():
    frame = make_frame()
    set_pixel(frame, 8, 8, 50.0)
    set_pixel(frame, 9, 9, 50.0)           # touches only on a diagonal
    hs = hotspots.find_hotspots(frame, threshold_c=35.0, min_pixels=1)
    assert len(hs) == 2
