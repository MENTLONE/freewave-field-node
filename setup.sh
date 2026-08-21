#!/bin/bash

set -e

echo
echo "=========================================="
echo " FREEWAVE SIGNAL SOCIETY"
echo " FIELD NODE INSTALLER"
echo "=========================================="
echo

# --------------------------------------------------
# Installation paths
# --------------------------------------------------

PROJECT_DIR="$HOME/freewave-field-node"
SERVICE_NAME="freewave-field-node"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

CURRENT_USER="$(id -un)"
CURRENT_GROUP="$(id -gn)"

echo "Installation user:"
echo "  $CURRENT_USER"
echo

echo "Installation directory:"
echo "  $PROJECT_DIR"
echo

# --------------------------------------------------
# 1. Update package lists
# --------------------------------------------------

echo "[1/7] Updating package lists..."

sudo apt update

# --------------------------------------------------
# 2. Install required system packages
# --------------------------------------------------

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

# --------------------------------------------------
# 3. Verify repository
# --------------------------------------------------

echo
echo "[3/7] Checking FreeWave repository..."

if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo
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

# --------------------------------------------------
# 4. Create Python virtual environment
# --------------------------------------------------

echo
echo "[4/7] Creating Python virtual environment..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

# --------------------------------------------------
# 5. Install Python dependencies
# --------------------------------------------------

echo
echo "[5/7] Installing Python dependencies..."

source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

deactivate

# --------------------------------------------------
# 6. Install dynamic systemd service
# --------------------------------------------------

echo
echo "[6/7] Installing FreeWave systemd service..."

echo
echo "Generating systemd service for:"
echo "  User:       $CURRENT_USER"
echo "  Group:      $CURRENT_GROUP"
echo "  Directory:  $PROJECT_DIR"
echo

sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=FreeWave Signal Society Field Node
After=local-fs.target dev-ttyACM0.device
Wants=dev-ttyACM0.device

[Service]
Type=simple
User=$CURRENT_USER
Group=$CURRENT_GROUP
WorkingDirectory=$PROJECT_DIR

ExecStart=$PROJECT_DIR/.venv/bin/python $PROJECT_DIR/src/main.py

Restart=on-failure
RestartSec=5

TTYPath=/dev/tty1
StandardInput=tty
StandardOutput=tty
StandardError=journal

Environment=TERM=linux

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"

# --------------------------------------------------
# 7. Installation complete
# --------------------------------------------------

echo
echo "[7/7] Installation complete."

echo
echo "=========================================="
echo " FREEWAVE FIELD NODE INSTALLED"
echo "=========================================="
echo

echo "User:"
echo "  $CURRENT_USER"

echo
echo "Repository:"
echo "  $PROJECT_DIR"

echo
echo "Virtual environment:"
echo "  $PROJECT_DIR/.venv"

echo
echo "Service:"
echo "  $SERVICE_NAME"

echo
echo "Service file:"
echo "  $SERVICE_FILE"

echo
echo "To start FreeWave now:"
echo
echo "  sudo systemctl start $SERVICE_NAME"

echo
echo "To check the service:"
echo
echo "  sudo systemctl status $SERVICE_NAME --no-pager"

echo
echo "To view logs:"
echo
echo "  sudo journalctl -u $SERVICE_NAME -n 100 --no-pager"

echo
echo "To follow live logs:"
echo
echo "  sudo journalctl -u $SERVICE_NAME -f"

echo
echo "=========================================="
echo " INSTALLATION READY"
echo "=========================================="
echo
