import os
import struct
import select
import threading


class FreeWaveTouch:
    """Very small FT5x06 touchscreen reader."""

    DEVICE = "/dev/input/event5"

    FORMAT = "llHHI"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self):
        self.running = False
        self.thread = None

        self.lock = threading.Lock()
        self.queue = []

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._reader,
            daemon=True,
        )

        self.thread.start()

    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join(timeout=1)

        self.thread = None

    def get_touch(self):
        with self.lock:
            if not self.queue:
                return None

            return self.queue.pop(0)

    def _reader(self):
        try:
            fd = os.open(
                self.DEVICE,
                os.O_RDONLY | os.O_NONBLOCK,
            )
        except OSError:
            self.running = False
            return

        x = None
        y = None
        touching = False

        try:
            while self.running:

                ready, _, _ = select.select(
                    [fd],
                    [],
                    [],
                    0.25,
                )

                if not ready:
                    continue

                try:
                    data = os.read(
                        fd,
                        self.SIZE,
                    )
                except BlockingIOError:
                    continue

                if len(data) != self.SIZE:
                    continue

                _, _, event_type, code, value = struct.unpack(
                    self.FORMAT,
                    data,
                )

                # Absolute X
                if event_type == 3 and code == 53:
                    x = value

                # Absolute Y
                elif event_type == 3 and code == 54:
                    y = value

                # Touch press/release
                elif event_type == 1 and code == 330:

                    if value == 1:
                        touching = True

                    elif value == 0 and touching:

                        if x is not None and y is not None:
                            with self.lock:
                                self.queue.append(
                                    (x, y)
                                )

                        touching = False

        finally:
            try:
                os.close(fd)
            except OSError:
                pass
