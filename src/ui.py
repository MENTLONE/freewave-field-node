import curses

from status import (
    get_cpu_temperature,
    get_memory,
    get_uptime,
    format_uptime,
)


class FreeWaveUI:
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
            stdscr.addstr(10, 4, "Q  QUIT")

            self.draw_footer(stdscr)

            stdscr.refresh()

            key = stdscr.getch()

            if key in (ord("q"), ord("Q")):
                break

            elif key == ord("2"):
                self.nodes_screen(stdscr)

            elif key == ord("3"):
                self.status_screen(stdscr)

            elif key == ord("4"):
                self.radio_screen(stdscr)

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

    def nodes_screen(self, stdscr):
        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            stdscr.addstr(5, 4, "NODES")
            stdscr.addstr(6, 4, "-" * 70)

            nodes = self.radio.get_nodes()

            row = 8

            for node in nodes[:20]:
                user = node.get("user", {})

                name = user.get("longName", "UNKNOWN")
                short_name = user.get("shortName", "----")
                node_id = user.get("id", "--------")

                name = name[:28]
                short_name = short_name[:8]

                stdscr.addstr(
                    row,
                    4,
                    f"{short_name:<8} {name:<28} {node_id}",
                )

                row += 1

                if row >= stdscr.getmaxyx()[0] - 4:
                    break

            self.draw_footer(stdscr)

            stdscr.addstr(
                stdscr.getmaxyx()[0] - 3,
                4,
                "B  BACK",
            )

            stdscr.refresh()

            key = stdscr.getch()

            if key in (ord("b"), ord("B")):
                return

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

            stdscr.addstr(row, 4, "RASPBERRY PI")
            row += 2

            if temp is not None:
                stdscr.addstr(row, 6, f"CPU TEMP:       {temp:.1f} C")

            row += 1

            if memory:
                stdscr.addstr(
                    row,
                    6,
                    f"MEMORY:         {memory['used']} / {memory['total']} MB",
                )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"UPTIME:         {format_uptime(uptime)}",
            )

            row += 2

            stdscr.addstr(row, 4, "RADIO")
            row += 2

            stdscr.addstr(
                row,
                6,
                f"MODEL:          {info.get('hardware', 'UNKNOWN')}",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"NODE:           {info.get('long_name', 'UNKNOWN')}",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"BATTERY:        {info.get('battery', 'UNKNOWN')}%",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"VOLTAGE:        {info.get('voltage', 'UNKNOWN')} V",
            )

            row += 2

            stdscr.addstr(row, 4, "MESH")
            row += 2

            stdscr.addstr(
                row,
                6,
                f"NODES:          {self.radio.get_node_count()}",
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

            if key in (ord("b"), ord("B")):
                return

            if key in (ord("r"), ord("R")):
                continue

    def radio_screen(self, stdscr):
        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            stdscr.addstr(5, 4, "RADIO INFORMATION")
            stdscr.addstr(6, 4, "-" * 70)

            info = self.radio.get_local_info()

            row = 8

            stdscr.addstr(row, 4, "CONNECTION")
            row += 2

            stdscr.addstr(
                row,
                6,
                "STATUS:         CONNECTED",
            )

            row += 2

            stdscr.addstr(row, 4, "DEVICE")
            row += 2

            stdscr.addstr(
                row,
                6,
                f"MODEL:          {info.get('hardware', 'UNKNOWN')}",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"NODE NAME:      {info.get('long_name', 'UNKNOWN')}",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"SHORT NAME:     {info.get('short_name', 'UNKNOWN')}",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"NODE ID:        {info.get('node_id', 'UNKNOWN')}",
            )

            row += 2

            stdscr.addstr(row, 4, "RADIO TELEMETRY")
            row += 2

            stdscr.addstr(
                row,
                6,
                f"BATTERY:        {info.get('battery', 'UNKNOWN')}%",
            )

            row += 1

            stdscr.addstr(
                row,
                6,
                f"VOLTAGE:        {info.get('voltage', 'UNKNOWN')} V",
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

            if key in (ord("b"), ord("B")):
                return

            if key in (ord("r"), ord("R")):
                continue
