"""Find hot spots in a temperature frame. Pure functions: no files, no network.

A frame is a flat list of 768 temperatures in Celsius: 24 rows x 32 columns,
row by row. The pixel at column x, row y lives at index y * 32 + x
(row 0 is the top of the image, facing north).
"""


def find_hotspots(frame, threshold_c=35.0, min_pixels=1, width=32, height=24):
    """Return the hotspots found in `frame`, hottest first.

    A hotspot is a group of pixels that are all STRICTLY ABOVE threshold_c
    and that touch each other up/down/left/right (4 neighbours). Touching
    only on a diagonal does NOT count as touching.

    Each hotspot is a record (the project convention):
      x, y   - centre pixel: mean of the blob's x values and mean of its y
               values, rounded to the nearest integer
      pixels - how many pixels are in the group
      max_c  - hottest temperature in the group

    Groups with fewer than `min_pixels` pixels are ignored.
    """
    if len(frame) != width * height:
        raise ValueError("frame has %d values, expected %d" % (len(frame), width * height))

    # Step 1: which pixels are hot? Strictly greater than the threshold,
    # so a pixel exactly at threshold_c is NOT hot.
    hot = [t > threshold_c for t in frame]
    seen = [False] * len(frame)
    hotspots = []

    # Step 2: walk the pixels in order. Every hot pixel we have not visited
    # yet starts a new flood fill that swallows its whole touching group.
    for start in range(len(frame)):
        if not hot[start] or seen[start]:
            continue
        stack = [start]          # pixels still to visit; pop from the end
        seen[start] = True
        count = 0
        total_x = total_y = 0
        max_c = frame[start]
        while stack:
            i = stack.pop()
            x, y = i % width, i // width
            count += 1
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
        if count < min_pixels:
            continue

        hotspots.append({
            "x": round(total_x / count),
            "y": round(total_y / count),
            "pixels": count,
            "max_c": round(max_c, 1),
        })

    hotspots.sort(key=lambda h: -h["max_c"])  # hottest first
    return hotspots
