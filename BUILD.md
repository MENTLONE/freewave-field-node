# FreeWave Signal Society Field Node
## Physical Build Guide

This guide documents the physical construction of the
FreeWave Signal Society Field Node.

The goal is to make the field node reproducible using the
hardware documented in `BOM.md`.

---

# 1. System Overview

The FreeWave Field Node is a portable Raspberry Pi-based
Meshtastic field terminal.

The system consists of:

- Raspberry Pi 3B+
- 5-inch DSI touchscreen
- Heltec WiFi LoRa 32 V4
- USB connection between Raspberry Pi and Heltec
- Small USB power bank
- Protective Pelican case
- Custom 3D-printed internal holding bracket

The Raspberry Pi runs the FreeWave user interface.

The Heltec V4 provides the Meshtastic LoRa radio.

The touchscreen provides the field operator interface.

The entire system is designed to operate as a portable,
self-contained field communication terminal.

---

# 2. Hardware Architecture

```text
                  ┌──────────────────────┐
                  │   5" DSI TOUCHSCREEN │
                  └──────────┬───────────┘
                             │
                            DSI
                             │
                  ┌──────────▼───────────┐
                  │   RASPBERRY PI 3B+   │
                  │                      │
                  │   FreeWave UI        │
                  │   Field Terminal     │
                  └──────────┬───────────┘
                             │
                            USB
                             │
                  ┌──────────▼───────────┐
                  │      HELTEC V4       │
                  │   ESP32-S3 / SX1262  │
                  │      Meshtastic      │
                  └──────────┬───────────┘
                             │
                            LoRa
                             │
                  ┌──────────▼───────────┐
                  │   MESHTASTIC MESH    │
                  └──────────────────────┘


                         POWER
                           │
                    ┌──────▼──────┐
                    │ USB POWER   │
                    │    BANK     │
                    └─────────────┘
3. Enclosure

The field node is designed around a compact Pelican protective
case.

Internal dimensions
Length: 8-1/8 inches
Width: 5-5/8 inches
Height: 3-3/4 inches

The internal component arrangement and custom printed insert
are designed around these dimensions.

The enclosure protects the electronics during transport and
field operation.

4. 3D-Printed Holding Bracket

The field node uses a custom 3D-printed insert/bracket to
organize and secure the electronics inside the case.

The production model is:

freewave insert face 7.0.stl

The STL should be stored in:

hardware/bracket/

Recommended repository path:

hardware/bracket/freewave insert face 7.0.stl

The bracket is a FreeWave Signal Society custom design.

Its purpose is to:

Position the Raspberry Pi
Position the Heltec radio
Organize internal wiring
Prevent components from moving inside the case
Maintain a repeatable internal layout
Make additional field nodes easier to reproduce
5. Printing the Bracket

The bracket should be printed using a durable 3D-printing
material appropriate for the intended environment.

Recommended starting parameters:

Material: PETG or equivalent durable filament
Layer height: 0.20 mm
Infill: 20–30%
Supports: Determine from the final STL geometry
Orientation: Flat on the largest stable surface

The exact print settings may be adjusted depending on the
printer and filament.

The physical dimensions of the final print should be checked
against the Pelican case before final assembly.

6. Raspberry Pi

Install the Raspberry Pi 3B+ into the custom internal bracket.

The Raspberry Pi is the primary computer for the field node.

It provides:

FreeWave graphical interface
Touchscreen control
Message display
Node display
Direct messaging
Persistent message history
Field presentation mode
Communication with the Heltec radio

The Raspberry Pi should be securely mounted so that it cannot
move inside the enclosure during transportation.

7. Touchscreen

Connect the 5-inch DSI touchscreen to the Raspberry Pi using
the appropriate DSI connection.

The touchscreen serves as the primary operator interface.

Before closing the enclosure, verify:

Display works
Touch input works
Display cable is secure
Cable routing does not interfere with the enclosure
The screen is positioned correctly relative to the case
8. Heltec WiFi LoRa 32 V4

Install the Heltec WiFi LoRa 32 V4 in the designated position
in the printed bracket.

The Heltec V4 provides:

ESP32-S3 processing
SX1262 LoRa radio
Meshtastic firmware
Wireless mesh communication

Connect the Heltec to the Raspberry Pi using USB.

The Raspberry Pi should detect the radio as a serial device.

Typical device:

/dev/ttyACM0

The actual device name should be verified on each installation.

9. USB Connection

Connect the Raspberry Pi to the Heltec V4 using a USB data cable.

The cable must support data communication.

A charge-only USB cable will not work.

Before final enclosure assembly:

ls /dev/ttyACM*

Verify that the Heltec radio is detected.

10. Power

The field node is designed for portable operation.

A small USB power bank provides the primary field power source.

The power bank should provide sufficient continuous power for
the Raspberry Pi and connected hardware.

Before field deployment:

Fully charge the power bank
Verify the USB cable
Verify the Raspberry Pi remains powered
Verify the touchscreen remains operational
Verify the Heltec remains connected
Test the node under normal operating conditions

Actual operating time depends on:

Power-bank capacity
Display brightness
Raspberry Pi workload
Radio activity
USB conversion efficiency
Battery condition
11. Internal Cable Management

Keep internal cables organized and secured.

Cable routing should:

Avoid touchscreen mounting points
Avoid the Raspberry Pi cooling area
Avoid stressing the DSI cable
Avoid stressing the Heltec USB connector
Avoid interfering with the case closure
Allow the electronics to remain securely positioned

Do not allow loose cables to become trapped when closing
the enclosure.

12. Antenna

The Heltec radio requires its appropriate LoRa antenna to be
connected before radio operation.

Do not operate the radio without the appropriate antenna
connected.

Route the antenna connection so that it is not mechanically
stressed by the enclosure or internal bracket.

13. Final Assembly

Recommended assembly sequence:

Print the custom FreeWave bracket.
Verify the bracket fits the Pelican case.
Install the Raspberry Pi.
Install the Heltec V4.
Install the touchscreen.
Connect the DSI cable.
Connect the USB data cable between the Pi and Heltec.
Connect the power system.
Organize and secure internal cables.
Verify the Heltec antenna connection.
Power the system.
Verify the FreeWave software starts.
Verify touchscreen operation.
Verify the Meshtastic radio connection.
Verify nodes appear.
Verify messaging.
Close the enclosure and verify that nothing is pinched.
14. Functional Test

Before considering the physical build complete, perform a
complete functional test.

Raspberry Pi

Verify:

Raspberry Pi boots
FreeWave starts automatically
Display works
Touchscreen works
No unexpected software errors
Heltec

Verify:

Heltec powers on
USB connection works
Meshtastic firmware is running
Radio connection is detected
Mesh

Verify:

Mesh nodes appear
Node information updates
Messages can be viewed
Direct messages can be sent
Power

Verify:

Power bank powers the complete system
System remains stable
USB connections remain secure
Enclosure

Verify:

Electronics remain stationary
Cables are not pinched
Case closes correctly
Touchscreen remains accessible
15. Field Deployment Configuration

The completed system should operate as a self-contained
portable field terminal.

┌─────────────────────────────────────────┐
│          FREEWAVE FIELD NODE            │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │        5" TOUCHSCREEN             │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │        RASPBERRY PI 3B+           │  │
│  └───────────────────────────────────┘  │
│                    │                    │
│                   USB                   │
│                    │                    │
│  ┌─────────────────▼─────────────────┐  │
│  │           HELTEC V4               │  │
│  │        MESHTASTIC RADIO           │  │
│  └───────────────────────────────────┘  │
│                                         │
│        USB POWER BANK                   │
│                                         │
└─────────────────────────────────────────┘

The entire assembly is housed inside the protective case.

16. Replication

The physical design is intended to be reproducible.

A second field node should be constructible using:

BOM.md
BUILD.md
INSTALL.md
FIELD-CHECKLIST.md
The custom bracket STL
The FreeWave software repository

The goal is to allow another builder to reproduce the system
without requiring access to the original development machine.

17. Design Philosophy

FreeWave Signal Society is intended to demonstrate that useful
communication infrastructure can be built from accessible
hardware and open-source software.

The field node combines:

Raspberry Pi computing
Touchscreen interfaces
Meshtastic
LoRa radio
3D-printed hardware
Portable power
Open-source software

The result is a compact, portable platform for experimenting
with off-grid communication and distributed mesh networks.

Current Build

FreeWave Signal Society - Chicago Division

Field Node 1

Presentation-ready physical build.

Software baseline:

v1.0.0 / Milestone 9 known-good presentation build

Repository documentation should remain synchronized with the
physical production node.
