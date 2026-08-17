import curses

from status import (
    get_cpu_temperature,
    get_memory,
    get_uptime,
    format_uptime,
)


class FreeWaveUI:
    """Curses-based FreeWave Signal Society field-node interface."""

    def __init__(self, radio):
        self.radio = radio

    def run(self):
        curses.wrapper(self._main)

    def _main(self, stdscr):
        curses.curs_set(0)

        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            stdscr.addstr(5, 4, "1  MESSAGES")
            stdscr.addstr(6, 4, "2  NODES")
            stdscr.addstr(7, 4, "3  STATUS")
            stdscr.addstr(8, 4, "4  RADIO")
            stdscr.addstr(9, 4, "5  SEND MESSAGE")
            stdscr.addstr(11, 4, "Q  QUIT")

            self.draw_footer(stdscr)

            stdscr.refresh()

            key = stdscr.getch()

            if key in (ord("q"), ord("Q")):
                break

            elif key == ord("1"):
                self.messages_screen(stdscr)

            elif key == ord("2"):
                self.nodes_screen(stdscr)

            elif key == ord("3"):
                self.status_screen(stdscr)

            elif key == ord("4"):
                self.radio_screen(stdscr)

            elif key == ord("5"):
                self.send_message_screen(stdscr)

    def draw_header(self, stdscr):
        stdscr.addstr(0, 2, "FREEWAVE SIGNAL SOCIETY")
        stdscr.addstr(1, 2, "CHICAGO DIVISION — FIELD NODE")
        stdscr.addstr(3, 2, "-" * 70)

    def draw_footer(self, stdscr):
        height, _ = stdscr.getmaxyx()

        stdscr.addstr(
            height - 2,
            2,
            f"RADIO: CONNECTED    MESH: {self.radio.get_node_count()} NODES",
        )

    # ------------------------------------------------------------------
    # MESSAGES
    # ------------------------------------------------------------------

    def messages_screen(self, stdscr):
        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            stdscr.addstr(5, 4, "MESSAGES")
            stdscr.addstr(6, 4, "-" * 70)

            messages = self.radio.get_messages()

            row = 8

            if not messages:
                stdscr.addstr(
                    row,
                    4,
                    "NO MESSAGES RECEIVED",
                )
            else:
                for message in messages:
                    timestamp = message.get("time", "--:--:--")
                    direction = message.get("direction", "RX")

                    if direction == "TX":
                        sender = "LOCAL"
                    else:
                        sender_id = message.get("from")
                        sender = self.get_sender_name(sender_id)

                    text_msg = str(message.get("text", ""))
                    text_msg = text_msg.replace("\n", " ")

                    max_width = max(
                        20,
                        stdscr.getmaxyx()[1] - 28,
                    )

                    if len(text_msg) > max_width:
                        text_msg = text_msg[:max_width - 3] + "..."

                    try:
                        stdscr.addstr(
                            row,
                            4,
                            f"{timestamp}  {direction:<2}  "
                            f"{sender:<12} {text_msg}",
                        )
                    except curses.error:
                        pass

                    row += 1

                    if row >= stdscr.getmaxyx()[0] - 4:
                        break

            self.draw_footer(stdscr)

            stdscr.addstr(
                stdscr.getmaxyx()[0] - 3,
                4,
                "B  BACK     R  REFRESH",
            )

            stdscr.refresh()

            key = stdscr.getch()

            if key in (ord("b"), ord("B")):
                return

            if key in (ord("r"), ord("R")):
                continue

    def get_sender_name(self, node_id):
        if not node_id:
            return "UNKNOWN"

        for node in self.radio.get_nodes():
            user = node.get("user", {})

            if user.get("id") == node_id:
                return user.get(
                    "shortName",
                    user.get("longName", node_id),
                )[:12]

        return str(node_id)[:12]

    # ------------------------------------------------------------------
    # SEND MESSAGE
    # ------------------------------------------------------------------

    def send_message_screen(self, stdscr):
        """Compose a broadcast or direct Meshtastic message."""

        message = ""
        destination = "^all"
        destination_name = "BROADCAST"

        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            stdscr.addstr(5, 4, "SEND MESSAGE")
            stdscr.addstr(6, 4, "-" * 70)

            stdscr.addstr(
                8,
                4,
                f"DESTINATION: {destination_name}",
            )

            stdscr.addstr(
                9,
                4,
                f"NODE ID:     {destination}",
            )

            stdscr.addstr(11, 4, "MESSAGE:")
            stdscr.addstr(12, 4, "> " + message)

            stdscr.addstr(
                stdscr.getmaxyx()[0] - 4,
                4,
                "N  SELECT NODE     ENTER  SEND     B  CANCEL",
            )

            self.draw_footer(stdscr)
            stdscr.refresh()

            key = stdscr.getch()

            if key in (ord("b"), ord("B")):
                return

            # Select destination.
            if key in (ord("n"), ord("N")):
                selected = self.select_destination(stdscr)

                if selected:
                    destination, destination_name = selected

                continue

            # Backspace.
            if key in (curses.KEY_BACKSPACE, 127, 8):
                message = message[:-1]
                continue

            # Send.
            if key in (curses.KEY_ENTER, 10, 13):
                if not message.strip():
                    continue

                try:
                    self.radio.send_message(
                        message,
                        destination=destination,
                    )
                except Exception as exc:
                    self.show_error(
                        stdscr,
                        f"SEND ERROR: {str(exc)[:55]}",
                    )
                    continue

                return

            # Normal printable character.
            if 32 <= key <= 126:
                if len(message) < 200:
                    message += chr(key)

    # ------------------------------------------------------------------
    # DESTINATION SELECTOR
    # ------------------------------------------------------------------

    def select_destination(self, stdscr):
        """Display live mesh nodes and return (node_id, display_name)."""

        nodes = self.radio.get_nodes()

        entries = [
            {
                "id": "^all",
                "short": "ALL",
                "long": "BROADCAST",
                "num": None,
            }
        ]

        for node in nodes:
            user = node.get("user", {})

            node_id = user.get("id")

            if not node_id:
                continue

            # Don't offer our own node as a direct destination.
            if node_id == self.radio.get_node_id():
                continue

            entries.append(
                {
                    "id": node_id,
                    "short": user.get("shortName", "----"),
                    "long": user.get(
                        "longName",
                        node_id,
                    ),
                    "num": node.get("num"),
                }
            )

        if not entries:
            return None

        selected = 0
        top = 0

        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            stdscr.addstr(
                5,
                4,
                "SELECT DESTINATION",
            )

            stdscr.addstr(
                6,
                4,
                "-" * 70,
            )

            stdscr.addstr(
                7,
                4,
                "UP/DOWN  SELECT     ENTER  CHOOSE     B  CANCEL",
            )

            height, width = stdscr.getmaxyx()

            visible_rows = max(
                5,
                height - 12,
            )

            if selected < top:
                top = selected

            if selected >= top + visible_rows:
                top = selected - visible_rows + 1

            for screen_row, index in enumerate(
                range(
                    top,
                    min(
                        len(entries),
                        top + visible_rows,
                    ),
                )
            ):
                entry = entries[index]

                prefix = ">" if index == selected else " "

                short_name = str(
                    entry["short"]
                )[:8]

                long_name = str(
                    entry["long"]
                )[:32]

                node_id = str(
                    entry["id"]
                )[:12]

                line = (
                    f"{prefix} {short_name:<8} "
                    f"{long_name:<32} {node_id}"
                )

                try:
                    stdscr.addstr(
                        9 + screen_row,
                        4,
                        line[:max(20, width - 8)],
                    )
                except curses.error:
                    pass

            self.draw_footer(stdscr)

            stdscr.refresh()

            key = stdscr.getch()

            if key in (
                ord("b"),
                ord("B"),
                27,
            ):
                return None

            if key in (
                curses.KEY_UP,
                ord("k"),
            ):
                selected = max(
                    0,
                    selected - 1,
                )

            elif key in (
                curses.KEY_DOWN,
                ord("j"),
            ):
                selected = min(
                    len(entries) - 1,
                    selected + 1,
                )

            elif key in (
                curses.KEY_ENTER,
                10,
                13,
            ):
                entry = entries[selected]

                return (
                    entry["id"],
                    entry["short"]
                    if entry["id"] != "^all"
                    else "BROADCAST",
                )

    def show_error(self, stdscr, text):
        height, _ = stdscr.getmaxyx()

        try:
            stdscr.addstr(
                height - 5,
                4,
                text,
            )
            stdscr.addstr(
                height - 4,
                4,
                "PRESS ANY KEY",
            )
        except curses.error:
            pass

        stdscr.refresh()
        stdscr.getch()

    # ------------------------------------------------------------------
    # NODES
    # ------------------------------------------------------------------

    def nodes_screen(self, stdscr):
        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            stdscr.addstr(5, 4, "NODES")
            stdscr.addstr(6, 4, "-" * 70)

            nodes = self.radio.get_nodes()

            row = 8

            for node in nodes:
                user = node.get("user", {})

                name = user.get(
                    "longName",
                    "UNKNOWN",
                )

                short_name = user.get(
                    "shortName",
                    "----",
                )

                node_id = user.get(
                    "id",
                    "--------",
                )

                name = str(name)[:28]
                short_name = str(short_name)[:8]

                try:
                    stdscr.addstr(
                        row,
                        4,
                        f"{short_name:<8} "
                        f"{name:<28} "
                        f"{node_id}",
                    )
                except curses.error:
                    pass

                row += 1

                if row >= stdscr.getmaxyx()[0] - 4:
                    break

            self.draw_footer(stdscr)

            stdscr.addstr(
                stdscr.getmaxyx()[0] - 3,
                4,
                "B  BACK     R  REFRESH",
            )

            stdscr.refresh()

            key = stdscr.getch()

            if key in (
                ord("b"),
                ord("B"),
            ):
                return

            if key in (
                ord("r"),
                ord("R"),
            ):
                continue

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def status_screen(self, stdscr):
        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            stdscr.addstr(5, 4, "SYSTEM STATUS")
            stdscr.addstr(6, 4, "-" * 70)

            temp = get_cpu_temperature()
            memory = get_memory()
            uptime = get_uptime()
            info = self.radio.get_local_info()

            row = 8

            stdscr.addstr(
                row,
                4,
                "RASPBERRY PI",
            )
            row += 2

            if temp is not None:
                stdscr.addstr(
                    row,
                    6,
                    f"CPU TEMP:       {temp:.1f} C",
                )

            row += 1

            if memory:
                stdscr.addstr(
                    row,
                    6,
                    f"MEMORY:         "
                    f"{memory['used']} / "
                    f"{memory['total']} MB",
                )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"UPTIME:         "
                f"{format_uptime(uptime)}",
            )

            row += 2

            stdscr.addstr(
                row,
                4,
                "RADIO",
            )
            row += 2

            stdscr.addstr(
                row,
                6,
                f"MODEL:          "
                f"{info.get('hardware', 'UNKNOWN')}",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"NODE:           "
                f"{info.get('long_name', 'UNKNOWN')}",
            )

            row += 1

            battery = info.get(
                "battery",
                "UNKNOWN",
            )

            stdscr.addstr(
                row,
                6,
                f"BATTERY:        {battery}%",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"VOLTAGE:        "
                f"{info.get('voltage', 'UNKNOWN')} V",
            )

            row += 2

            stdscr.addstr(
                row,
                4,
                "MESH",
            )
            row += 2

            stdscr.addstr(
                row,
                6,
                f"NODES:          "
                f"{self.radio.get_node_count()}",
            )

            row += 2

            stdscr.addstr(
                row,
                4,
                "B  BACK     R  REFRESH",
            )

            self.draw_footer(stdscr)

            stdscr.refresh()

            key = stdscr.getch()

            if key in (
                ord("b"),
                ord("B"),
            ):
                return

            if key in (
                ord("r"),
                ord("R"),
            ):
                continue

    # ------------------------------------------------------------------
    # RADIO
    # ------------------------------------------------------------------

    def radio_screen(self, stdscr):
        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            stdscr.addstr(
                5,
                4,
                "RADIO INFORMATION",
            )

            stdscr.addstr(
                6,
                4,
                "-" * 70,
            )

            info = self.radio.get_local_info()

            row = 8

            stdscr.addstr(
                row,
                4,
                "CONNECTION",
            )
            row += 2

            stdscr.addstr(
                row,
                6,
                "STATUS:         CONNECTED",
            )

            row += 2

            stdscr.addstr(
                row,
                4,
                "DEVICE",
            )
            row += 2

            stdscr.addstr(
                row,
                6,
                f"MODEL:          "
                f"{info.get('hardware', 'UNKNOWN')}",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"NODE NAME:      "
                f"{info.get('long_name', 'UNKNOWN')}",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"SHORT NAME:     "
                f"{info.get('short_name', 'UNKNOWN')}",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"NODE ID:        "
                f"{info.get('node_id', 'UNKNOWN')}",
            )

            row += 2

            stdscr.addstr(
                row,
                4,
                "RADIO TELEMETRY",
            )
            row += 2

            stdscr.addstr(
                row,
                6,
                f"BATTERY:        "
                f"{info.get('battery', 'UNKNOWN')}%",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"VOLTAGE:        "
                f"{info.get('voltage', 'UNKNOWN')} V",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"UPTIME:         "
                f"{info.get('uptime', 'UNKNOWN')} sec",
            )

            row += 2

            stdscr.addstr(
                row,
                4,
                "MESH",
            )
            row += 2

            stdscr.addstr(
                row,
                6,
                f"NODES:          "
                f"{self.radio.get_node_count()}",
            )

            row += 2

            stdscr.addstr(
                row,
                4,
                "B  BACK     R  REFRESH",
            )

            self.draw_footer(stdscr)

            stdscr.refresh()

            key = stdscr.getch()

            if key in (
                ord("b"),
                ord("B"),
            ):
                return

            if key in (
                ord("r"),
                ord("R"),
            ):
                continue
