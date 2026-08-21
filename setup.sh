#!/bin/bash

set -e

echo
echo "=========================================="
echo " FREEWAVE SIGNAL SOCIETY"
echo " FIELD NODE INSTALLER"
echo "=========================================="
echo

PROJECT_DIR="$HOME/freewave-field-node"

echo "[1/7] Updating package lists..."
sudo apt update

echo
echo "[2/7] Installing required system packages..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-pygame \
    python3-tk \
    fonts-dejavu \
    fbi \
    git

echo
echo "[3/7] Checking FreeWave repository..."

if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo "FreeWave repository not found at:"
    echo "  $PROJECT_DIR"
    echo
    echo "Clone the repository first:"
    echo
    echo "  git clone git@github.com:MENTLONE/freewave-field-node.git"
    echo
    exit 1
fi

cd "$PROJECT_DIR"

echo
echo "[4/7] Creating Python virtual environment..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

echo
echo "[5/7] Installing Python dependencies..."

source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

deactivate

echo
echo "[6/7] Installing FreeWave systemd service..."

sudo cp \
    systemd/freewave-field-node.service \
    /etc/systemd/system/freewave-field-node.service

sudo systemctl daemon-reload

sudo systemctl enable freewave-field-node

echo
echo "[7/7] Installation complete."
echo
echo "=========================================="
echo " FREEWAVE FIELD NODE INSTALLED"
echo "=========================================="
echo
echo "Repository:"
echo "  $PROJECT_DIR"
echo
echo "Service:"
echo "  freewave-field-node"
echo
echo "To start FreeWave now:"
echo
echo "  sudo systemctl start freewave-field-node"
echo
echo "To check the service:"
echo
echo "  sudo systemctl status freewave-field-node --no-pager"
echo
echo "To view logs:"
echo
echo "  sudo journalctl -u freewave-field-node -n 100 --no-pager"
echo
