# FreeWave Signal Society Field Node
## Installation Guide

This guide describes how to install the FreeWave Signal Society Field Node
software on a Raspberry Pi.

The FreeWave field node uses a Raspberry Pi as the computer and user
interface, connected by USB to a Heltec WiFi LoRa 32 V4 running Meshtastic.

---

## 1. Hardware

The current field-node build uses:

- Raspberry Pi 3B+
- Heltec WiFi LoRa 32 V4
- 5-inch DSI touchscreen
- microSD card
- USB data cable
- Small USB power bank
- Pelican protective case
- Custom 3D-printed holding bracket

See `BOM.md` for the complete bill of materials.

---

## 2. Raspberry Pi Operating System

Install Raspberry Pi OS on the microSD card.

The Raspberry Pi should have:

- Network access during installation
- SSH enabled for maintenance
- A working user account
- The touchscreen connected
- The Heltec V4 connected by USB

After installation, update the operating system:

    sudo apt update
    sudo apt upgrade -y

---

## 3. Required System Packages

Install the packages required by FreeWave:

    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-pygame \
        python3-tk \
        fonts-dejavu \
        fbi \
        git

---

## 4. Clone the Repository

Clone the FreeWave repository:

    git clone git@github.com:MENTLONE/freewave-field-node.git

Enter the project directory:

    cd ~/freewave-field-node

---

## 5. Python Virtual Environment

Create the Python virtual environment:

    python3 -m venv .venv

Activate it:

    source .venv/bin/activate

---

## 6. Install Python Dependencies

With the virtual environment activated:

    pip install --upgrade pip
    pip install -r requirements.txt

The current project requirements are:

    meshtastic==2.7.11
    pyserial==3.5

---

## 7. Verify the Heltec Radio

Connect the Heltec WiFi LoRa 32 V4 to the Raspberry Pi by USB.

Check the available serial devices:

    ls /dev/ttyACM*

The FreeWave system service currently expects:

    /dev/ttyACM0

If the Heltec appears as `/dev/ttyACM0`, the radio connection is ready.

---

## 8. Test the Application Manually

From the project directory with the virtual environment activated:

    python src/main.py

Verify that:

- The FreeWave splash screen appears
- The FreeWave interface launches
- The touchscreen responds
- The Heltec radio connects
- Mesh nodes appear
- Messages can be viewed
- Direct messaging functions correctly

Use `Ctrl+C` to stop the application during manual testing.

---

## 9. Install the systemd Service

The repository contains:

    systemd/freewave-field-node.service

Copy it into the systemd service directory:

    sudo cp systemd/freewave-field-node.service \
        /etc/systemd/system/freewave-field-node.service

Reload systemd:

    sudo systemctl daemon-reload

Enable the FreeWave service:

    sudo systemctl enable freewave-field-node

Start the service:

    sudo systemctl start freewave-field-node

---

## 10. Verify the Service

Check the service:

    sudo systemctl status freewave-field-node --no-pager

The expected state is:

    Active: active (running)

Check whether it starts automatically:

    sudo systemctl is-enabled freewave-field-node

The expected result is:

    enabled

---

## 11. View FreeWave Logs

View recent FreeWave service messages:

    sudo journalctl -u freewave-field-node -n 100 --no-pager

Follow the live log:

    sudo journalctl -u freewave-field-node -f

Look for Python exceptions, radio connection errors, or repeated service
restarts.

---

## 12. Verify Automatic Boot

After installation, reboot the Raspberry Pi:

    sudo reboot

The FreeWave field node should automatically:

1. Boot Raspberry Pi OS
2. Start the FreeWave systemd service
3. Display the FreeWave splash
4. Launch the FreeWave field interface
5. Connect to the Heltec Meshtastic radio
6. Display the field-node interface

---

## 13. GitHub Updates

The FreeWave repository is maintained through Git.

Check the current version:

    git log -1 --oneline

Check the working tree:

    git status

Pull updates from GitHub:

    git pull origin main

Before updating a working field node, create a backup or verify that the
current working version has been committed to Git.

---

## 14. Field Deployment

Before taking the node into the field, verify:

- Raspberry Pi boots correctly
- FreeWave starts automatically
- Touchscreen works
- Heltec V4 is detected
- Meshtastic connection is active
- Nodes are visible
- Message transmission works
- Power bank is charged
- Display and USB connections are secure
- Electronics are secured inside the enclosure

---

## 15. Current FreeWave Baseline

The presentation-ready software baseline is the GitHub-backed Milestone 9
state.

Current repository history includes:

- Milestone 1 — Working field node terminal
- Milestone 2 — Meshtastic message viewer
- Milestone 3 — Message transmission
- Milestone 4 — Improved field message console
- Milestone 5 — Direct node messaging
- Milestone 6 — Persistent message history
- Milestone 7 — Boot directly into FreeWave field terminal
- Milestone 8 — Reliable node selection and direct messaging
- Milestone 9 — Touchscreen UI and FreeWave presentation mode

The working presentation version should be treated as a known-good baseline.

---

## Project

FreeWave Signal Society  
Chicago Division

A field-node project for learning, building, and experimenting with
Meshtastic networks, off-grid communication, Raspberry Pi systems, and
open-source hardware/software.
