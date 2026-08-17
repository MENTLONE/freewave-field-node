# FREEWAVE FIELD NODE

## FreeWave Signal Society — Chicago Division

A minimal Raspberry Pi field terminal for a Meshtastic LoRa radio.

The Raspberry Pi acts as the field-unit "head" while a Heltec V4 provides the Meshtastic radio connection.

## Design Goals

- Simple
- Green monochrome terminal UI
- No animations
- No unnecessary graphics
- No Wi-Fi required for LoRa communications
- SSH maintenance
- Easily reproducible from GitHub
- Field-serviceable

## Hardware

- Raspberry Pi
- Heltec WiFi LoRa 32 V4
- USB connection between Raspberry Pi and Heltec
- Optional display and keyboard

## Current Features

- Meshtastic radio connection
- Heltec V4 detection
- Live mesh node list
- Raspberry Pi system status
- Radio status
- Terminal-based UI

## Software

- Raspberry Pi OS
- Python 3
- Meshtastic Python API
- PySerial
- curses

## Project Structure

    freewave-field-node/
    ├── README.md
    ├── requirements.txt
    ├── .gitignore
    └── src/
        ├── main.py
        ├── message_test.py
        ├── radio.py
        ├── radio_test.py
        ├── status.py
        └── ui.py

## Hardware Architecture

    Raspberry Pi
          |
          | USB
          |
      Heltec V4
          |
          | LoRa
          |
      Meshtastic Mesh

## Status

### Milestone 1 — Working

- [x] Raspberry Pi environment
- [x] Python virtual environment
- [x] Meshtastic API
- [x] Heltec V4 connection
- [x] Live node list
- [x] System status
- [x] Radio status
- [x] Monochrome terminal UI

### Planned

- [ ] Message viewer
- [ ] Message transmission
- [ ] Robust radio reconnect
- [ ] Field logging
- [ ] Installation script
- [ ] One-command setup

## License

GPL-3.0
