# FREEWAVE FIELD NODE

## FreeWave Signal Society — Chicago Division

**A portable Raspberry Pi + Meshtastic field communication terminal.**

FreeWave Signal Society Field Node is an open-source hardware and software
project built around a Raspberry Pi and a Heltec WiFi LoRa 32 V4.

The Raspberry Pi acts as the field-unit "head," providing the user interface,
touchscreen control, system status, node information, message history, and
direct messaging.

The Heltec V4 provides the Meshtastic LoRa radio connection.

The result is a compact, portable field terminal designed for experimentation
with off-grid communication, LoRa mesh networks, open-source hardware, and
field-deployable computing.

---

# What Is FreeWave?

FreeWave Signal Society explores practical, accessible communication systems
that can operate outside conventional internet infrastructure.

The field node combines:

- Raspberry Pi computing
- Meshtastic
- LoRa radio
- Touchscreen interface
- Portable USB power
- 3D-printed hardware
- Open-source software
- Protective field enclosure

The system is designed to be understandable, reproducible, serviceable, and
easy to modify.

---

# Current Build

**FreeWave Signal Society — Chicago Division**

**Field Node 1**

### Software baseline

**v1.0.0 — Milestone 9 known-good presentation build**

The v1.0.0 release represents the presentation-ready software baseline.

The physical field node is housed in a compact Pelican protective case and
uses a custom 3D-printed internal holding bracket.

---

# Current Features

The current FreeWave field-node software provides:

- Meshtastic radio connection
- Heltec V4 detection
- Live mesh node list
- Node selection
- Direct messaging
- Message history
- Persistent message history
- Raspberry Pi system status
- Radio status
- Touchscreen interface
- FreeWave presentation mode
- Green monochrome terminal-style interface
- Automatic system startup
- systemd service management
- Field-oriented operation

---

# Hardware

The current production field node uses:

- Raspberry Pi 3B+
- Heltec WiFi LoRa 32 V4
- ESP32-S3 / SX1262 LoRa radio
- 5-inch DSI touchscreen
- microSD card
- USB data connection
- Small USB power bank
- Pelican protective case
- Custom 3D-printed internal holding bracket

The custom enclosure insert is designed around the following Pelican case
internal dimensions:

- **8-1/8 inches length**
- **5-5/8 inches width**
- **3-3/4 inches height**

See:

**[BOM.md](BOM.md)**

for the complete bill of materials.

---

# Hardware Architecture

```text
                  5" DSI TOUCHSCREEN
                           |
                          DSI
                           |
                           v
                  +-------------------+
                  |  RASPBERRY PI 3B+ |
                  |                   |
                  |    FREEWAVE UI    |
                  |   FIELD TERMINAL  |
                  +---------+---------+
                            |
                           USB
                            |
                            v
                  +-------------------+
                  |     HELTEC V4     |
                  | ESP32-S3 / SX1262 |
                  |     MESHTASTIC     |
                  +---------+---------+
                            |
                           LoRa
                            |
                            v
                     MESHTASTIC MESH


                      USB POWER BANK
                            |
                            v
                     FIELD NODE POWER

Documentation

The repository now contains documentation for both software and physical
construction.

Bill of Materials

BOM.md

Complete hardware list including:

Raspberry Pi
Heltec V4
Touchscreen
Power bank
Pelican case
Custom 3D-printed bracket
Supporting equipment
Physical Build Guide

BUILD.md

Documents:

Physical architecture
Case dimensions
Bracket
Component placement
Wiring
Power
Cable management
Assembly
Functional testing
Field deployment
Software Installation

INSTALL.md

Documents installation of:

Raspberry Pi OS
Required system packages
Python environment
Meshtastic dependencies
FreeWave software
systemd service
Automatic startup
Field Deployment

FIELD-CHECKLIST.md

Provides a pre-deployment checklist for taking the field node into operation.

Quick Start

A new Raspberry Pi can install the FreeWave software from the repository.

Clone the repository:

git clone git@github.com:MENTLONE/freewave-field-node.git
cd freewave-field-node

Run the installer:

chmod +x setup.sh
./setup.sh

The installer:

Updates Raspberry Pi OS packages
Installs required system packages
Creates the Python virtual environment
Installs pinned Python dependencies
Installs the FreeWave systemd service
Enables automatic startup

See INSTALL.md for the complete installation procedure.

Starting FreeWave

After installation:

sudo systemctl start freewave-field-node

Check the service:

sudo systemctl status freewave-field-node --no-pager

View recent logs:

sudo journalctl -u freewave-field-node -n 100 --no-pager

Follow the live log:

sudo journalctl -u freewave-field-node -f

Automatic Startup

The FreeWave systemd service is enabled during installation.

Verify:

sudo systemctl is-enabled freewave-field-node

Expected:

enabled

The intended field-node boot sequence is:

Raspberry Pi
      |
      v
Raspberry Pi OS
      |
      v
FreeWave systemd service
      |
      v
FreeWave splash
      |
      v
FreeWave field terminal
      |
      v
Heltec Meshtastic radio
      |
      v
Meshtastic mesh

Project Structure
freewave-field-node/
│
├── README.md
├── BOM.md
├── BUILD.md
├── INSTALL.md
├── FIELD-CHECKLIST.md
├── requirements.txt
├── setup.sh
│
├── freewave-splash-800x480.png
├── freewave green logo 1.0.png
│
├── src/
│   ├── main.py
│   ├── message_test.py
│   ├── radio.py
│   ├── radio_test.py
│   ├── status.py
│   ├── touch.py
│   └── ui.py
│
├── systemd/
│   └── freewave-field-node.service
│
└── hardware/
    └── bracket/
Development Milestones

The FreeWave field node was developed incrementally.

Milestone 1 — Working Field Node Terminal
Raspberry Pi environment
Python virtual environment
Meshtastic API
Heltec V4 connection
Live node list
System status
Radio status
Monochrome terminal UI
Milestone 2 — Meshtastic Message Viewer

Added message viewing and field-oriented communication display.

Milestone 3 — Message Transmission

Added the ability to transmit messages through the Meshtastic radio.

Milestone 4 — Improved Field Message Console

Improved the communication interface for field use.

Milestone 5 — Direct Node Messaging

Added direct messaging to individual mesh nodes.

Milestone 6 — Persistent Message History

Added persistent message history.

Milestone 7 — Boot Directly Into FreeWave Field Terminal

Configured the Raspberry Pi to launch directly into the FreeWave field
terminal environment.

Milestone 8 — Reliable Node Selection and Direct Messaging

Improved node selection and direct messaging behavior.

Milestone 9 — Touchscreen UI and FreeWave Presentation Mode

Added the touchscreen-oriented interface and presentation mode used by the
current field node.

v1.0.0

FreeWave Field Node v1.0.0

The v1.0.0 tag represents the known-good Milestone 9 presentation build.

This version should be treated as the protected baseline for future
development.

Future experimental changes should be developed from this baseline rather
than modifying the known-good build without a backup or checkpoint.

Design Goals

FreeWave is intentionally designed around a few principles:

Simple

The system should remain understandable and serviceable.

Reproducible

Another builder should be able to construct a field node using the repository
documentation and hardware list.

Field-Serviceable

The system should be repairable and maintainable without requiring specialized
infrastructure.

Open

The project uses accessible hardware and open-source software wherever
practical.

Off-Grid Capable

Meshtastic LoRa communication does not require an internet connection for the
mesh itself.

Portable

The field node is designed to operate from a small USB power bank inside a
protective enclosure.

Field Deployment

Before taking the node into the field, verify:

Raspberry Pi boots correctly
FreeWave starts automatically
Touchscreen works
Heltec V4 is detected
Meshtastic connection is active
Antenna is connected
Mesh nodes are visible
Messaging works
Power bank is charged
USB connections are secure
Electronics are secured inside the enclosure
Case closes without pinching cables

See FIELD-CHECKLIST.md.

Project Philosophy

FreeWave Signal Society is a practical exploration of communication,
electronics, computing, fabrication, and open-source technology.

The project is intended to demonstrate that a useful field communication
terminal can be built from accessible components and documented well enough
for others to reproduce.

The objective is not simply to build one working device.

The objective is to build a system that can be:

understood, reproduced, modified, repaired, and deployed.

FreeWave Signal Society

Chicago Division

Field Node 1

Built for experimentation with:

Meshtastic networks
LoRa communication
Off-grid communication
Raspberry Pi systems
Touchscreen interfaces
3D-printed hardware
Open-source software
Portable field technology
License

GPL-3.0
