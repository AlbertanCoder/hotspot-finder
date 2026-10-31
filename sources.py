"""Where thermal frames come from.

Every source has the same read() method returning one frame, so the rest of the
program never has to know whether the numbers came from a real camera or not.
"""
import random

WIDTH = 32
HEIGHT = 24
BACKGROUND_C = 18.0
NOISE_C = 0.4  # real sensors flicker, so the fake one does too
BLOB_RADIUS = 2.5  # pixels


class FakeCamera:
    """Pretends to be the thermal camera, for working without any hardware."""

    def __init__(self):
        self.blobs = [self._new_blob() for _ in range(random.randint(1, 3))]

    def _new_blob(self):
        return {
            "x": random.uniform(4, WIDTH - 5),
            "y": random.uniform(4, HEIGHT - 5),
            "x_speed": random.uniform(-0.3, 0.3),  # pixels per frame
            "y_speed": random.uniform(-0.3, 0.3),
            "temperature": random.uniform(40, 80),
        }

    def read(self):
        """Return one frame: a flat list of 768 temperatures, row by row."""
        self._move_blobs()
        frame = []
        for y in range(HEIGHT):
            for x in range(WIDTH):
                temperature = BACKGROUND_C + random.uniform(-NOISE_C, NOISE_C)
                for blob in self.blobs:
                    if self._is_inside(blob, x, y):
                        temperature = blob["temperature"] + random.uniform(-NOISE_C, NOISE_C)
                # One decimal place, the same as the real board prints.
                frame.append(round(temperature, 1))
        return frame

    def _move_blobs(self):
        for blob in self.blobs:
            blob["x"] += blob["x_speed"]
            blob["y"] += blob["y_speed"]
            # Reverse at the edges so a blob never drifts out of view for good.
            if not 0 <= blob["x"] <= WIDTH - 1:
                blob["x_speed"] = -blob["x_speed"]
            if not 0 <= blob["y"] <= HEIGHT - 1:
                blob["y_speed"] = -blob["y_speed"]

    def _is_inside(self, blob, x, y):
        distance_squared = (x - blob["x"]) ** 2 + (y - blob["y"]) ** 2
        return distance_squared <= BLOB_RADIUS ** 2


def make_camera(mode):
    """Pick the frame source named in config.py."""
    if mode == "fake":
        return FakeCamera()
    raise ValueError(f'MODE "{mode}" is not built yet. Use "fake" until Step 3.')
