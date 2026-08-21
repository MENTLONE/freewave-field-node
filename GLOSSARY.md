# FreeWave Signal Society Field Node
## Glossary of Terms

This glossary explains the technical terms used throughout the
FreeWave Signal Society Field Node project.

The goal is to make the project understandable to people who may be
new to Raspberry Pi, LoRa, Meshtastic, Linux, or field communications.

---

## A

### API

**Application Programming Interface**

A set of functions and programming interfaces that allow one piece of
software to communicate with another.

FreeWave uses the Meshtastic Python API to communicate with the Heltec
radio.

---

## B

### Baud Rate

The speed at which serial communication occurs.

USB-connected serial devices use a configured communication rate to
exchange data.

---

### BOM

**Bill of Materials**

A list of the hardware and components required to build a device.

FreeWave's hardware BOM is documented in:

    BOM.md

---

## C

### CLI

**Command-Line Interface**

A text-based interface where commands are entered into a terminal.

The Raspberry Pi can be administered through the CLI using SSH or a
local terminal.

---

### curses

A Python interface for creating terminal-based graphical user
interfaces.

The original FreeWave interface was designed around a monochrome
terminal-style UI.

---

## D

### DSI

**Display Serial Interface**

A Raspberry Pi display interface used to connect compatible displays
directly to the Raspberry Pi.

The FreeWave Field Node uses a 5-inch DSI touchscreen.

---

## E

### ESP32

A family of low-cost microcontrollers developed by Espressif.

The Heltec WiFi LoRa 32 V4 uses an ESP32-S3 microcontroller.

---

## F

### Field Node

A portable communications device designed to operate outside a
traditional fixed communications environment.

In the FreeWave project, the Field Node consists of:

- Raspberry Pi
- Touchscreen
- Heltec LoRa radio
- Portable power
- Protective enclosure
- Custom 3D-printed mounting hardware

---

### FreeWave Signal Society

The project and community identity behind the FreeWave Field Node.

FreeWave explores accessible technologies for:

- Off-grid communication
- LoRa mesh networking
- Open-source hardware
- Raspberry Pi systems
- Portable computing
- Field-deployable technology

---

## G

### GPIO

**General Purpose Input/Output**

Electrical pins on a computer or microcontroller that can be used to
interface with electronic hardware.

The FreeWave radio connection currently uses USB rather than GPIO.

---

## H

### Heltec WiFi LoRa 32 V4

The LoRa radio hardware used by the FreeWave Field Node.

The V4 combines:

- ESP32-S3
- SX1262 LoRa transceiver
- Wi-Fi
- Bluetooth
- OLED display
- USB connectivity

FreeWave uses the Heltec primarily as the Meshtastic LoRa radio.

---

### Head

The Raspberry Pi portion of the FreeWave Field Node.

The Raspberry Pi acts as the computational "head" of the system while
the Heltec provides the LoRa radio.

---

## I

### Installer

A script that prepares a computer to run the FreeWave software.

The repository includes:

    setup.sh

The installer:

- Installs required system packages
- Creates the Python virtual environment
- Installs Python dependencies
- Installs the systemd service
- Enables automatic startup

---

## L

### LoRa

**Long Range**

A radio technology designed for long-range, low-power communication.

LoRa is the physical radio technology used by Meshtastic.

---

### LoRa Mesh

A network in which LoRa devices communicate with one another and can
relay information through other nodes.

This allows messages to travel beyond the direct radio range between
two devices.

---

## M

### Meshtastic

An open-source system for communicating over LoRa radios without
requiring cellular service or conventional internet connectivity.

Meshtastic provides the networking and messaging layer used by the
FreeWave Field Node.

---

### Mesh Network

A network in which devices can communicate with multiple other devices
and potentially relay traffic through the network.

Meshtastic nodes can form a decentralized mesh network.

---

### microSD

A small removable flash-memory card commonly used as storage for
Raspberry Pi operating systems.

The FreeWave Raspberry Pi boots its operating system and software from
a microSD card.

---

## O

### OLED

**Organic Light-Emitting Diode**

A display technology commonly used in small embedded electronics.

The Heltec WiFi LoRa 32 V4 includes a small OLED display.

---

## P

### Pelican Case

A rugged protective equipment enclosure.

The FreeWave Field Node is designed around a compact Pelican case with
approximately:

- Length: 8-1/8 inches
- Width: 5-5/8 inches
- Height: 3-3/4 inches

The custom 3D-printed internal bracket is designed around these
dimensions.

---

### Python

The programming language used for the FreeWave Field Node software.

The primary application is located in:

    src/main.py

---

### Python Virtual Environment

An isolated Python software environment used to install project-specific
Python packages without modifying the system-wide Python installation.

FreeWave creates:

    .venv/

---

## R

### Raspberry Pi

A small single-board computer produced by Raspberry Pi.

The current FreeWave Field Node uses a:

**Raspberry Pi 3B+**

The Raspberry Pi provides:

- Processing
- Storage
- User interface
- Touchscreen control
- System monitoring
- Meshtastic application interface

---

### Radio

The hardware responsible for transmitting and receiving wireless
signals.

In the FreeWave Field Node, the Heltec V4 provides the LoRa radio.

---

### Repeater

A node that receives and retransmits network traffic to extend the
effective range of a communications network.

Meshtastic nodes can participate in mesh routing depending on their
configuration and role.

---

## S

### Serial

A method of transmitting data sequentially between electronic devices.

The Raspberry Pi communicates with the Heltec V4 through a USB serial
connection.

---

### SX1262

A LoRa transceiver chip manufactured by Semtech.

The Heltec WiFi LoRa 32 V4 uses the SX1262 for LoRa radio
communication.

---

### systemd

The service manager used by modern Linux systems, including Raspberry
Pi OS.

FreeWave uses a systemd service to automatically start the field-node
software.

The service is:

    freewave-field-node.service

---

### systemd Service

A configuration that tells Linux how to start, stop, restart, and
manage an application.

FreeWave's service automatically launches the field-node software during
system startup.

---

## T

### Touchscreen

A display that also detects physical touch input.

The FreeWave Field Node uses a 5-inch DSI touchscreen as its primary
user interface.

---

### Terminal

A text-based computer interface.

The FreeWave UI uses a terminal-inspired green monochrome design.

---

### TTY

**TeleTYpe**

A Linux terminal device.

FreeWave uses `/dev/tty1` for its primary field-terminal display.

---

## U

### USB

**Universal Serial Bus**

A standard interface for connecting electronic devices.

The FreeWave Raspberry Pi uses USB to connect to the Heltec V4 and to
provide power and data connections.

---

## V

### v1.0.0

The first tagged FreeWave Field Node release.

The current v1.0.0 release represents the known-good Milestone 9
presentation build.

---

### Virtual Environment

See:

**Python Virtual Environment**

---

## W

### Wi-Fi

A wireless networking technology commonly used for local network and
internet connectivity.

FreeWave's LoRa communication does not depend on Wi-Fi.

Wi-Fi may still be used for:

- Initial setup
- Software updates
- SSH maintenance
- Development

---

## 3D Printing

Additive manufacturing in which physical objects are produced
layer-by-layer from a digital model.

The FreeWave Field Node uses a custom 3D-printed internal holding
bracket.

The physical build is documented in:

    BUILD.md

---

## Off-Grid Communication

Communication that does not depend on conventional infrastructure such
as cellular networks or the public internet.

Meshtastic allows compatible LoRa devices to exchange messages over
radio-based mesh networks.

---

## Field Deployment

Operating the FreeWave Field Node away from the development workbench.

A field deployment may involve:

- Portable battery power
- Protective enclosure
- Touchscreen operation
- LoRa mesh communication
- Minimal network infrastructure

See:

    FIELD-CHECKLIST.md

---

## Repository

The Git repository containing the FreeWave project's source code,
documentation, hardware information, and deployment tools.

The repository includes:

    README.md
    BOM.md
    BUILD.md
    INSTALL.md
    FIELD-CHECKLIST.md
    GLOSSARY.md
    LICENSE
    setup.sh
    requirements.txt
    src/
    systemd/

---

## Known-Good

A version of the software that has been tested and confirmed to work as
intended.

The FreeWave project maintains known-good checkpoints during
development.

These local development checkpoints are intentionally excluded from the
public Git repository.

---

## Milestone

A significant development stage in the FreeWave project.

Milestones document the progression of the field node from its initial
working terminal through the current touchscreen presentation system.

---

## Field Node 1

The first physical FreeWave Signal Society field-node unit.

The current presentation-ready hardware is designated:

**FreeWave Signal Society — Chicago Division — Field Node 1**

---

## Project Philosophy

FreeWave is intended to be more than a single working device.

The goal is to create a system that can be:

**understood, reproduced, modified, repaired, and deployed.**
