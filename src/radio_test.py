from meshtastic.serial_interface import SerialInterface

PORT = "/dev/ttyACM0"

print()
print("======================================")
print(" FREEWAVE SIGNAL SOCIETY")
print(" CHICAGO DIVISION")
print(" RADIO TEST")
print("======================================")
print()
print(f"Connecting to {PORT}...")
print()

interface = SerialInterface(devPath=PORT)

print("CONNECTED")
print()

# Basic radio information
if interface.myInfo:
    node_num = interface.myInfo.my_node_num
    print(f"Node ID:       !{node_num:08x}")

# Find our node in the node database
node_id = f"!{interface.myInfo.my_node_num:08x}"
node = interface.nodes.get(node_id)

if node:
    user = node.get("user", {})
    metrics = node.get("deviceMetrics", {})

    print(f"Name:          {user.get('longName', 'Unknown')}")
    print(f"Short name:    {user.get('shortName', 'Unknown')}")
    print(f"Hardware:      {user.get('hwModel', 'Unknown')}")

    if metrics:
        print(f"Battery:       {metrics.get('batteryLevel', 'Unknown')}%")
        print(f"Voltage:       {metrics.get('voltage', 'Unknown')} V")
        print(f"Uptime:        {metrics.get('uptimeSeconds', 'Unknown')} sec")

print()
print(f"Nodes in mesh: {len(interface.nodes)}")
print()
print("FREEWAVE RADIO: READY")
print()

interface.close()
