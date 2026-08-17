from meshtastic.serial_interface import SerialInterface


class FreeWaveRadio:
    """Small wrapper around the Meshtastic Python API."""

    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.interface = None

    def connect(self):
        self.interface = SerialInterface(devPath=self.port)

    def close(self):
        if self.interface:
            self.interface.close()
            self.interface = None

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
