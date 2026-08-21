from collections import deque
from datetime import datetime
from pathlib import Path
import json
import threading

from pubsub import pub
from meshtastic.serial_interface import SerialInterface


class FreeWaveRadio:
    """Small, defensive wrapper around the Meshtastic Python API."""

    def __init__(
        self,
        port="/dev/ttyACM0",
        message_log="data/messages.jsonl",
    ):
        self.port = port
        self.interface = None
        self.messages = deque(maxlen=100)

        self.message_log = Path(message_log)
        self.message_log.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._lock = threading.RLock()
        self._connected = False

        self.load_message_history()

    # ------------------------------------------------------------------
    # RADIO CONNECTION
    # ------------------------------------------------------------------

    def connect(self):
        """Connect to the Meshtastic radio."""

        with self._lock:
            if self.interface is not None:
                return

            # Subscribe before opening the serial interface so that
            # messages arriving immediately during startup are not missed.
            pub.subscribe(
                self._on_message,
                "meshtastic.receive.text",
            )

            try:
                self.interface = SerialInterface(
                    devPath=self.port
                )
                self._connected = True

            except Exception:
                self.interface = None
                self._connected = False

                try:
                    pub.unsubscribe(
                        self._on_message,
                        "meshtastic.receive.text",
                    )
                except Exception:
                    pass

                raise

    def close(self):
        """Cleanly close the radio connection."""

        with self._lock:
            try:
                pub.unsubscribe(
                    self._on_message,
                    "meshtastic.receive.text",
                )
            except Exception:
                pass

            if self.interface:
                try:
                    self.interface.close()
                except Exception:
                    pass

            self.interface = None
            self._connected = False

    def is_connected(self):
        """Return True when the radio interface is active."""

        return bool(
            self.interface is not None
            and self._connected
        )

    # ------------------------------------------------------------------
    # MESSAGE PERSISTENCE
    # ------------------------------------------------------------------

    def save_message(self, message):
        """Append one message to the persistent JSONL log."""

        try:
            with self.message_log.open(
                "a",
                encoding="utf-8",
            ) as handle:
                handle.write(
                    json.dumps(
                        message,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

        except OSError:
            # Logging failure must never stop radio operation.
            pass

    def load_message_history(self):
        """Load recent messages from the persistent JSONL log."""

        if not self.message_log.exists():
            return

        try:
            with self.message_log.open(
                "r",
                encoding="utf-8",
            ) as handle:

                for line in handle:
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        message = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if isinstance(message, dict):
                        self.messages.append(message)

        except OSError:
            pass

    # ------------------------------------------------------------------
    # RECEIVE
    # ------------------------------------------------------------------

    def _on_message(self, packet, interface=None):
        """Receive a Meshtastic text message."""

        try:
            decoded = packet.get(
                "decoded",
                {},
            )

            text = decoded.get("text")

            if not text:
                return

            from_id = packet.get("from")
            to_id = packet.get("to")

            message = {
                "time": datetime.now().strftime(
                    "%H:%M:%S"
                ),
                "from": from_id,
                "to": to_id,
                "text": str(text),
                "direction": "RX",
            }

            with self._lock:
                self.messages.append(message)

            self.save_message(message)

        except Exception:
            # Never allow a malformed received packet to break
            # the FreeWave application.
            return

    # ------------------------------------------------------------------
    # MESSAGE ACCESS
    # ------------------------------------------------------------------

    def get_messages(self):
        """Return messages, newest first."""

        with self._lock:
            return list(
                reversed(self.messages)
            )

    # ------------------------------------------------------------------
    # TRANSMISSION
    # ------------------------------------------------------------------

    def send_message(
        self,
        text,
        destination="^all",
        want_ack=False,
    ):
        """Send a Meshtastic text message and record local TX."""

        with self._lock:
            if not self.interface:
                raise RuntimeError(
                    "Radio is not connected"
                )

            text = str(text).strip()

            if not text:
                raise ValueError(
                    "Message cannot be empty"
                )

            packet = self.interface.sendText(
                text,
                destinationId=destination,
                wantAck=want_ack,
            )

            message = {
                "time": datetime.now().strftime(
                    "%H:%M:%S"
                ),
                "from": self.get_node_id(),
                "to": destination,
                "text": text,
                "direction": "TX",
            }

            self.messages.append(message)

            self.save_message(message)

            return packet

    # ------------------------------------------------------------------
    # NODE INFORMATION
    # ------------------------------------------------------------------

    def get_node_id(self):
        """Return the local Meshtastic node ID."""

        with self._lock:
            if not self.interface:
                return None

            if not self.interface.myInfo:
                return None

            return (
                f"!{self.interface.myInfo.my_node_num:08x}"
            )

    def get_nodes(self):
        """Return the current node database."""

        with self._lock:
            if not self.interface:
                return []

            try:
                return list(
                    self.interface.nodes.values()
                )
            except Exception:
                return []

    def get_node_count(self):
        """Return the number of known mesh nodes."""

        return len(
            self.get_nodes()
        )

    def get_local_node(self):
        """Return the local node record."""

        node_id = self.get_node_id()

        if not node_id:
            return None

        with self._lock:
            if not self.interface:
                return None

            try:
                return self.interface.nodes.get(
                    node_id
                )
            except Exception:
                return None

    def get_local_info(self):
        """Return useful information about the local node."""

        node = self.get_local_node()

        if not node:
            return {}

        user = node.get(
            "user",
            {},
        )

        metrics = node.get(
            "deviceMetrics",
            {},
        )

        return {
            "id": node.get("num"),
            "node_id": user.get(
                "id",
                "Unknown",
            ),
            "long_name": user.get(
                "longName",
                "Unknown",
            ),
            "short_name": user.get(
                "shortName",
                "Unknown",
            ),
            "hardware": user.get(
                "hwModel",
                "Unknown",
            ),
            "battery": metrics.get(
                "batteryLevel"
            ),
            "voltage": metrics.get(
                "voltage"
            ),
            "uptime": metrics.get(
                "uptimeSeconds"
            ),
        }
