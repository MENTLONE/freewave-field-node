from meshtastic.serial_interface import SerialInterface
from pubsub import pub
import time

PORT = "/dev/ttyACM0"


def on_receive(packet, interface):
    decoded = packet.get("decoded", {})
    portnum = decoded.get("portnum")

    if portnum == "TEXT_MESSAGE_APP":
        text = decoded.get("payload", b"")

        try:
            text = text.decode("utf-8", errors="replace")
        except AttributeError:
            pass

        sender = packet.get("fromId", "UNKNOWN")

        print()
        print("======================================")
        print(" INCOMING MESSAGE")
        print("======================================")
        print(f"FROM: {sender}")
        print(f"TEXT: {text}")
        print("======================================")
        print()


pub.subscribe(on_receive, "meshtastic.receive")

print()
print("======================================")
print(" FREEWAVE MESSAGE TEST")
print("======================================")
print()
print(f"Connecting to {PORT}...")

interface = SerialInterface(devPath=PORT)

print("CONNECTED")
print()
print("Listening for Meshtastic messages...")
print("Press CTRL+C to exit.")
print()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print()
    print("Stopping...")

finally:
    interface.close()
