import subprocess
import time

from radio import FreeWaveRadio
from ui import FreeWaveUI


LOGO = "/home/mentlone/freewave-field-node/freewave-splash-800x480.png"


def show_splash():
    """Display the real FreeWave logo on the framebuffer for 4 seconds."""

    try:
        process = subprocess.Popen(
            [
                "sudo",
                "/usr/bin/fbi",
                "--noverbose",
                "--autofit",
                "--once",
                LOGO,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        time.sleep(7)

        process.terminate()

        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()

    except Exception:
        # Never prevent the field node from starting
        # just because the splash cannot be displayed.
        pass


def main():
    show_splash()

    radio = FreeWaveRadio()

    try:
        radio.connect()

        ui = FreeWaveUI(radio)
        ui.run()

    finally:
        radio.close()


if __name__ == "__main__":
    main()
