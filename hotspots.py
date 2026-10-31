"""Find hot spots in a temperature frame. Pure functions: no files, no network.

A frame is a flat list of 768 temperatures in Celsius: 24 rows x 32 columns,
row by row. The pixel at column x, row y lives at index y * 32 + x.
"""


def find_hotspots(frame, width=32, height=24, threshold_c=35.0, min_pixels=1):
    """Return the hotspots found in `frame`, hottest first.

    A hotspot is a group of pixels that are all ABOVE threshold_c and that
    touch each other up/down/left/right (4 neighbours). Touching only on a
    diagonal does NOT count as touching.

    Each hotspot is a dict:
      cx, cy  - centre pixel of the group (average of its pixels, rounded)
      count   - how many pixels are in the group
      max_c   - hottest temperature in the group
      pixels  - [[x, y], ...] every pixel in the group, for drawing outlines

    Groups with fewer than `min_pixels` pixels are ignored.
    """
    if len(frame) != width * height:
        raise ValueError("frame has %d values, expected %d" % (len(frame), width * height))

    # Step 1: which pixels are hot? Strictly ABOVE the threshold.
    hot = [t > threshold_c for t in frame]
    seen = [False] * len(frame)
    hotspots = []

    # Step 2: walk the pixels in order. Every hot pixel we have not visited
    # yet starts a new flood fill that swallows its whole touching group.
    for start in range(len(frame)):
        if not hot[start] or seen[start]:
            continue
        stack = [start]          # pixels to visit; pop from the end
        seen[start] = True
        pixels = []
        total_x = total_y = 0
        max_c = frame[start]
        while stack:
            i = stack.pop()
            x, y = i % width, i // width
            pixels.append((x, y))
            total_x += x
            total_y += y
            if frame[i] > max_c:
                max_c = frame[i]
            # The 4 neighbours: left, right, up, down. Not the diagonals.
            neighbours = []
            if x > 0:
                neighbours.append(i - 1)
            if x < width - 1:
                neighbours.append(i + 1)
            if y > 0:
                neighbours.append(i - width)
            if y < height - 1:
                neighbours.append(i + width)
            for n in neighbours:
                if hot[n] and not seen[n]:
                    seen[n] = True      # mark now so it is never queued twice
                    stack.append(n)

        # Step 3: too-small groups are noise, not hotspots.
        if len(pixels) < min_pixels:
            continue

        pixels.sort()  # row-major order, so output is predictable
        hotspots.append({
            "cx": round(total_x / len(pixels)),
            "cy": round(total_y / len(pixels)),
            "count": len(pixels),
            "max_c": round(max_c, 1),
            "pixels": [[x, y] for x, y in pixels],
        })

    hotspots.sort(key=lambda h: -h["max_c"])
    return hotspots
