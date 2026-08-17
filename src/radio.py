from collections import deque
from datetime import datetime
from pathlib import Path
import json

from pubsub import pub
from meshtastic.serial_interface import SerialInterface


class FreeWaveRadio:
    """Small wrapper around the Meshtastic Python API."""

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

        self.load_message_history()

    # ------------------------------------------------------------------
    # RADIO CONNECTION
    # ------------------------------------------------------------------

    def connect(self):
        self.interface = SerialInterface(devPath=self.port)

        pub.subscribe(
            self._on_message,
            "meshtastic.receive.text",
        )

    def close(self):
        if self.interface:
            try:
                pub.unsubscribe(
                    self._on_message,
                    "meshtastic.receive.text",
                )
            except Exception:
                pass

            self.interface.close()
            self.interface = None

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
            # A logging failure must never stop radio operation.
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

        decoded = packet.get("decoded", {})
        text = decoded.get("text")

        if not text:
            return

        from_id = packet.get("from")
        to_id = packet.get("to")

        message = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "from": from_id,
            "to": to_id,
            "text": str(text),
            "direction": "RX",
        }

        self.messages.append(message)
        self.save_message(message)

    # ------------------------------------------------------------------
    # MESSAGE ACCESS
    # ------------------------------------------------------------------

    def get_messages(self):
        """Return messages, newest first."""

        return list(reversed(self.messages))

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

        if not self.interface:
            raise RuntimeError("Radio is not connected")

        text = str(text).strip()

        if not text:
            raise ValueError("Message cannot be empty")

        packet = self.interface.sendText(
            text,
            destinationId=destination,
            wantAck=want_ack,
        )

        message = {
            "time": datetime.now().strftime("%H:%M:%S"),
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
        if not self.interface or not self.interface.myInfo:
            return None

        return f"!{self.interface.myInfo.my_node_num:08x}"

    def get_nodes(self):
        if not self.interface:
            return []

        return list(self.interface.nodes.values())

    def get_node_count(self):
        return len(self.get_nodes())

    def get_local_node(self):
        node_id = self.get_node_id()

        if not node_id:
            return None

        return self.interface.nodes.get(node_id)

    def get_local_info(self):
        node = self.get_local_node()

        if not node:
            return {}

        user = node.get("user", {})
        metrics = node.get("deviceMetrics", {})

        return {
            "id": node.get("num"),
            "node_id": user.get("id"),
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
            "battery": metrics.get("batteryLevel"),
            "voltage": metrics.get("voltage"),
            "uptime": metrics.get("uptimeSeconds"),
        }
