# FreeWave Signal Society Field Node
## Bill of Materials

The FreeWave Signal Society Field Node is a portable Raspberry Pi-based
Meshtastic field terminal. The Raspberry Pi provides the field-node computer
and user interface, while the Heltec V4 provides the Meshtastic LoRa radio.

---

## Core Electronics

| Item | Qty | Specification | Purpose |
|---|---:|---|---|
| Raspberry Pi | 1 | Raspberry Pi 3B+ | Main field-node computer |
| LoRa Radio | 1 | Heltec WiFi LoRa 32 V4 / ESP32-S3 / SX1262 | Meshtastic radio |
| Display | 1 | 5-inch DSI touchscreen | Main display and touch interface |
| microSD Card | 1 | Raspberry Pi-compatible | Raspberry Pi OS and FreeWave software |
| USB Data Cable | 1 | Raspberry Pi to Heltec compatible | Serial connection to radio |
| Power Bank | 1 | Small USB power bank | Portable field power |
| Power Cable | 1 | USB cable appropriate for Raspberry Pi 3B+ | Power from power bank |

---

## Enclosure

| Item | Qty | Specification | Purpose |
|---|---:|---|---|
| Pelican Case | 1 | 8-1/8 x 5-5/8 x 3-3/4 in internal dimensions | Protective field enclosure |
| 3D-Printed Holding Bracket | 1 | Custom FreeWave Signal Society design | Secures electronics inside case |

### Pelican Case Internal Dimensions

- Length: 8-1/8 in
- Width: 5-5/8 in
- Height: 3-3/4 in

The custom bracket and internal component layout are designed around these
dimensions.

---

## 3D-Printed Holding Bracket

The field node uses a custom 3D-printed bracket to hold and organize the
electronics inside the Pelican case.

The production STL should be included in the repository.

Recommended location:

    hardware/bracket/freewave-field-node-bracket.stl

When the final STL is added, this section should also document:

- Filament/material
- Layer height
- Infill
- Print orientation
- Supports, if required
- Number of printed parts
- Required mounting hardware

---

## Power

The field node is designed for portable operation using a small USB power
bank.

Actual operating time will depend on:

- Power-bank capacity
- Display brightness
- Raspberry Pi workload
- Meshtastic radio activity
- USB power efficiency
- Battery condition

The power bank should be capable of providing sufficient continuous USB
power for the Raspberry Pi and connected hardware.

---

## Hardware Architecture

    5-inch DSI Touchscreen
              |
              | DSI
              |
       Raspberry Pi 3B+
       FreeWave UI
              |
              | USB
              |
          Heltec V4
       ESP32-S3 / SX1262
          Meshtastic
              |
              | LoRa
              |
        Meshtastic Mesh

---

## Optional / Service Equipment

| Item | Qty | Purpose |
|---|---:|---|
| USB Keyboard | 1 | Setup and field maintenance |
| Spare USB Cable | 1 | Field replacement |
| Spare microSD Card | 1 | Recovery / backup |
| Spare Power Bank | 1 | Backup field power |
| Mounting Hardware | As required | Securing the 3D-printed bracket |

---

## Replication

The goal of this BOM is to make the FreeWave Field Node reproducible.

As the design is finalized, exact manufacturer names, model numbers, part
numbers, and fabrication files should be added where appropriate.

The BOM should be updated whenever the physical field-node design changes.

---

## Current Build

**FreeWave Signal Society - Chicago Division**

**Presentation-ready field node**

Software baseline: **Milestone 9 / merged GitHub repository state**

Hardware documentation should remain synchronized with the physical
production node.
