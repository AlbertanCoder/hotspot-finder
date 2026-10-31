"""Frame sources: where the 768 temperatures come from.

Every source will share one method:
    read_frame() -> list of width*height temperatures in Celsius

Step 1 has FakeCamera only. SerialCamera (real board) and ReplayCamera
(saved recordings) arrive in Step 3.
"""

import math
import random


class FakeCamera:
    """Makes up plausible thermal frames so the demo works without hardware.

    Each frame is background (~18 C with small noise) plus 1-3 hot blobs of
    40-80 C that drift slowly around the picture.
    """

    def __init__(self, width=32, height=24):
        self.width = width
        self.height = height
        # Fixed seed so the fake scene is the same every run: my tests and
        # Shad's screen recordings always agree on what the picture shows.
        random.seed(42)
        # Build the blobs once. They drift a little every frame; they do not
        # teleport, so the picture changes smoothly like a real scene would.
        self.blobs = []
        for _ in range(random.randint(1, 3)):
            self.blobs.append({
                "x": random.uniform(3, width - 4),
                "y": random.uniform(3, height - 4),
                "peak_c": random.uniform(40.0, 80.0),
            })

    def read_frame(self):
        """Return one frame: a flat list of width*height temperatures."""
        frame = [random.gauss(18.0, 0.4) for _ in range(self.width * self.height)]
        for blob in self.blobs:
            self._draw_blob(frame, blob)
            self._drift(blob)
        return frame

    def _draw_blob(self, frame, blob):
        """Add one round hot blob to the frame.

        Heat falls off like a bell curve from the centre, so only pixels near
        the middle get hot enough to pass the threshold. The blob adds
        (peak_c - 18) at its centre, so the centre pixel reaches about
        peak_c degrees.
        """
        sigma = 1.5   # blob fatness, in pixels
        reach = 4     # beyond this distance the heat is about zero
        cx, cy = blob["x"], blob["y"]
        heat = blob["peak_c"] - 18.0
        y0, y1 = max(0, int(cy) - reach), min(self.height, int(cy) + reach + 1)
        x0, x1 = max(0, int(cx) - reach), min(self.width, int(cx) + reach + 1)
        for y in range(y0, y1):
            for x in range(x0, x1):
                d2 = (x - cx) ** 2 + (y - cy) ** 2
                frame[y * self.width + x] += heat * math.exp(-d2 / (2 * sigma * sigma))

    def _drift(self, blob):
        """Move the blob one tiny random step, clamped to stay on the sensor."""
        blob["x"] = min(max(blob["x"] + random.uniform(-0.5, 0.5), 1.0), self.width - 2)
        blob["y"] = min(max(blob["y"] + random.uniform(-0.5, 0.5), 1.0), self.height - 2)
