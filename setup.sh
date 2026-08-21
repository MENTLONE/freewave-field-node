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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"

SERVICE_NAME="freewave-field-node"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

CURRENT_USER="$(id -un)"
CURRENT_GROUP="$(id -gn)"

echo "Installation user:"
echo "  $CURRENT_USER"
echo

echo "Installation group:"
echo "  $CURRENT_GROUP"
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
# 3. Check FreeWave repository
# --------------------------------------------------

echo
echo "[3/7] Checking FreeWave repository..."

if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo
    echo "ERROR: FreeWave repository not found."
    echo
    echo "Expected repository directory:"
    echo "  $PROJECT_DIR"
    echo
    echo "The installer must be run from inside"
    echo "a cloned FreeWave repository."
    echo
    echo "Example:"
    echo
    echo "  git clone https://github.com/MENTLONE/freewave-field-node.git"
    echo "  cd freewave-field-node"
    echo "  chmod +x setup.sh"
    echo "  ./setup.sh"
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

source "$PROJECT_DIR/.venv/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "$PROJECT_DIR/requirements.txt"

deactivate

# --------------------------------------------------
# 6. Install systemd service
# --------------------------------------------------

echo
echo "[6/7] Installing FreeWave systemd service..."

echo
echo "Generating service configuration:"
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

echo "Group:"
echo "  $CURRENT_GROUP"
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

echo "To view recent logs:"
echo
echo "  sudo journalctl -u $SERVICE_NAME -n 100 --no-pager"
echo

echo "To follow live logs:"
echo
echo "  sudo journalctl -u $SERVICE_NAME -f"
echo
