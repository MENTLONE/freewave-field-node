from collections import deque
from datetime import datetime

from pubsub import pub
from meshtastic.serial_interface import SerialInterface


class FreeWaveRadio:
    """Small wrapper around the Meshtastic Python API."""

    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.interface = None
        self.messages = deque(maxlen=100)

    def connect(self):
        self.interface = SerialInterface(devPath=self.port)

        pub.subscribe(
            self._on_message,
            "meshtastic.receive.text"
        )

    def close(self):
        if self.interface:
            try:
                pub.unsubscribe(
                    self._on_message,
                    "meshtastic.receive.text"
                )
            except Exception:
                pass

            self.interface.close()
            self.interface = None

    def _on_message(self, packet, interface=None):
        """Receive a Meshtastic text message."""

        decoded = packet.get("decoded", {})
        text = decoded.get("text")

        if not text:
            return

        from_id = packet.get("from")
        to_id = packet.get("to")
        rx_time = packet.get("rxTime")

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.messages.append({
            "time": timestamp,
            "from": from_id,
            "to": to_id,
            "text": text,
        })

    def get_messages(self):
        """Return received messages, newest first."""
        return list(reversed(self.messages))

    def send_message(self, text, destination="^all", want_ack=False):
        """Send a Meshtastic text message and record the local TX message."""

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

        # Record our own transmission locally so the UI immediately
        # shows what was sent, without waiting for a radio echo.
        self.messages.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "from": self.get_node_id(),
            "to": destination,
            "text": text,
            "direction": "TX",
        })

        return packet
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
            "long_name": user.get("longName", "Unknown"),
            "short_name": user.get("shortName", "Unknown"),
            "hardware": user.get("hwModel", "Unknown"),
            "battery": metrics.get("batteryLevel"),
            "voltage": metrics.get("voltage"),
            "uptime": metrics.get("uptimeSeconds"),
        }
