"""Tests for find_hotspots, on small hand-built frames.

Every test starts from a cool frame and heats named pixels, so you can read
exactly which pixels were hot and work out the right answer by hand.
"""
from hotspots import find_hotspots

WIDTH = 32
HEIGHT = 24
COOL = 18.0
HOT = 60.0
THRESHOLD = 35.0


def make_frame(hot_pixels, temperature=HOT):
    """Build a cool frame with the given (x, y) pixels set to a hot temperature."""
    frame = [COOL] * (WIDTH * HEIGHT)
    for x, y in hot_pixels:
        frame[y * WIDTH + x] = temperature
    return frame


def test_no_hotspot_in_a_cool_frame():
    assert find_hotspots(make_frame([]), THRESHOLD, 1) == []


def test_one_blob_is_counted_once():
    frame = make_frame([(10, 10), (11, 10), (10, 11), (11, 11)])
    frame[10 * WIDTH + 11] = 75.5  # one pixel hotter, to prove max_c finds it

    found = find_hotspots(frame, THRESHOLD, 1)

    assert len(found) == 1
    assert found[0]["x"] == 10.5  # the centre of a 2x2 block sits between pixels
    assert found[0]["y"] == 10.5
    assert found[0]["pixels"] == 4
    assert found[0]["max_c"] == 75.5


def test_two_separate_blobs():
    found = find_hotspots(make_frame([(2, 2), (3, 2), (20, 15)]), THRESHOLD, 1)

    assert len(found) == 2
    assert sorted(spot["pixels"] for spot in found) == [1, 2]


def test_diagonal_pixels_do_not_touch():
    # The spec joins pixels up, down, left and right only, so a corner-to-corner
    # pair is two hotspots.
    found = find_hotspots(make_frame([(5, 5), (6, 6)]), THRESHOLD, 1)

    assert len(found) == 2


def test_blob_touching_the_corner_of_the_frame():
    found = find_hotspots(make_frame([(0, 0), (1, 0), (0, 1)]), THRESHOLD, 1)

    assert len(found) == 1
    assert found[0]["pixels"] == 3


def test_right_edge_does_not_wrap_onto_the_next_row():
    # In the flat list, (31, 3) and (0, 4) are neighbours, but on the real image
    # they are on opposite sides. A sloppy fill would join them into one hotspot.
    found = find_hotspots(make_frame([(WIDTH - 1, 3), (0, 4)]), THRESHOLD, 1)

    assert len(found) == 2


def test_pixel_exactly_at_the_threshold_is_not_hot():
    # The spec says "above the threshold", so equal does not count.
    assert find_hotspots(make_frame([(4, 4)], THRESHOLD), THRESHOLD, 1) == []


def test_pixel_just_above_the_threshold_is_hot():
    assert len(find_hotspots(make_frame([(4, 4)], THRESHOLD + 0.1), THRESHOLD, 1)) == 1


def test_min_pixels_drops_small_blobs():
    frame = make_frame([(2, 2), (20, 15), (21, 15)])

    found = find_hotspots(frame, THRESHOLD, 2)

    assert len(found) == 1
    assert found[0]["pixels"] == 2
