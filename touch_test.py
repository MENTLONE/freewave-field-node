import struct

DEVICE = "/dev/input/event5"
FORMAT = "llHHI"
SIZE = struct.calcsize(FORMAT)

x = None
y = None
touching = False

print("======================================")
print(" FREEWAVE TOUCHSCREEN TEST")
print("======================================")
print()
print("Touch different places on the screen.")
print("I'll report X/Y coordinates.")
print()
print("Press Ctrl+C to exit.")
print()

with open(DEVICE, "rb") as f:
    while True:
        data = f.read(SIZE)

        if len(data) != SIZE:
            continue

        sec, usec, event_type, code, value = struct.unpack(
            FORMAT,
            data
        )

        # Absolute X
        if event_type == 3 and code == 53:
            x = value

        # Absolute Y
        elif event_type == 3 and code == 54:
            y = value

        # Finger/button
        elif event_type == 1 and code == 330:

            if value == 1:
                touching = True

            elif value == 0:
                if touching and x is not None and y is not None:
                    print(f"TOUCH: X={x:4}  Y={y:4}")

                touching = False

