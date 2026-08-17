from radio import FreeWaveRadio
from ui import FreeWaveUI


def main():
    radio = FreeWaveRadio()

    try:
        radio.connect()

        ui = FreeWaveUI(radio)
        ui.run()

    finally:
        radio.close()


if __name__ == "__main__":
    main()
