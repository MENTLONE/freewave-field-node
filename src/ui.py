import curses
from pathlib import Path
import time
from PIL import Image
from touch import FreeWaveTouch

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

        # Simple touchscreen input.
        # Keyboard input remains fully supported.
        self.touch = FreeWaveTouch()
        self.touch.start()

        self.touch_action = None

    def run(self):
        curses.wrapper(self._main)

    # ------------------------------------------------------------------
    # SPLASH SCREEN
    # ------------------------------------------------------------------

    def splash_screen(self, stdscr):
        """Display the FreeWave logo for four seconds at startup."""

        logo_path = Path(
            "/home/mentlone/freewave-field-node/"
            "freewave green logo 1.0.png"
        )

        stdscr.clear()

        height, width = stdscr.getmaxyx()

        try:
            # Load the actual logo.
            image = Image.open(logo_path).convert("L")

            # Convert the logo into a high-resolution terminal image.
            # This is intentionally much larger than the previous
            # character rendering so the logo is clearly visible.
            max_width = min(72, width - 2)
            max_height = min(30, height - 4)

            image.thumbnail(
                (max_width * 2, max_height),
                Image.Resampling.LANCZOS,
            )

            pixels = list(image.getdata())
            img_w, img_h = image.size

            chars = " .:-=+*#%@"

            for y in range(0, img_h, 2):

                line = ""

                for x in range(img_w):

                    top = pixels[y * img_w + x]

                    if y + 1 < img_h:
                        bottom = pixels[
                            (y + 1) * img_w + x
                        ]
                    else:
                        bottom = top

                    value = (top + bottom) // 2

                    index = int(
                        value * (len(chars) - 1) / 255
                    )

                    line += chars[index]

                col = max(
                    0,
                    (width - len(line)) // 2,
                )

                self.safe_addstr(
                    stdscr,
                    2 + (y // 2),
                    col,
                    line,
                    curses.A_BOLD,
                )

            self.safe_addstr(
                stdscr,
                height - 2,
                max(2, (width - 12) // 2),
                "FIELD NODE 1",
                curses.A_BOLD,
            )

        except Exception:

            # Safe fallback if the logo cannot be loaded.
            self.safe_addstr(
                stdscr,
                max(8, height // 2 - 2),
                max(2, (width - 32) // 2),
                "[ FREEWAVE SIGNAL SOCIETY ]",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                max(10, height // 2),
                max(2, (width - 28) // 2),
                "CHICAGO DIVISION",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                max(12, height // 2 + 2),
                max(2, (width - 12) // 2),
                "FIELD NODE 1",
                curses.A_BOLD,
            )

        stdscr.refresh()

        # Hold the splash for four seconds.
        time.sleep(4.0)

    # ------------------------------------------------------------------
    # MAIN MENU
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # TOUCH MENU
    # ------------------------------------------------------------------

    def handle_touch_menu(self, x, y):
        """
        Convert physical touchscreen coordinates into
        large, separated FreeWave menu buttons.

        Touchscreen:
            X = approximately 0..800
            Y = approximately 0..480

        The menu intentionally uses generous spacing so
        fingers are less likely to hit the wrong command.
        """

        # Ignore taps outside the left/center menu area.
        if x > 650:
            return False

        # --------------------------------------------------
        # LARGE TOUCH TARGETS
        # --------------------------------------------------
        #
        # Each button has a clear gap before the next one.
        #
        # 1 MESSAGES
        # 2 NODES
        # 3 STATUS
        # 4 RADIO
        # 5 SEND MESSAGE
        #
        # The gaps intentionally do NOTHING.
        # --------------------------------------------------

        if 65 <= y < 105:
            self._touch_action(1)

        elif 125 <= y < 165:
            self._touch_action(2)

        elif 185 <= y < 225:
            self._touch_action(3)

        elif 245 <= y < 290:
            self._touch_action(4)

        elif 315 <= y < 365:
            self._touch_action(5)

        elif 385 <= y < 435:
            self._touch_action(6)

        else:
            return False

        return True

    def _touch_action(self, action):
        """
        Store the selected menu action.

        The main curses loop processes it safely.
        """

        self.touch_action = action

    def _main(self, stdscr):
        curses.curs_set(0)

        stdscr.keypad(True)

        # Do not let keyboard input block touchscreen polling.
        # This allows the physical touchscreen and Bluetooth
        # keyboard to operate independently.
        stdscr.timeout(100)

        # --------------------------------------------------
        # FREEWAVE CRT PHOSPHOR GREEN
        # --------------------------------------------------
        curses.start_color()

        try:
            curses.use_default_colors()
        except curses.error:
            pass

        try:
            # Bright terminal green on true black.
            curses.init_pair(
                7,
                curses.COLOR_GREEN,
                curses.COLOR_BLACK,
            )
        except curses.error:
            pass

        while True:
            stdscr.clear()

            self.draw_header(stdscr)

            # --------------------------------------------------
            # LARGE TOUCH-FRIENDLY MAIN MENU
            # --------------------------------------------------
            #
            # Keep generous vertical spacing for finger input.
            # Keyboard numbers remain exactly the same.
            # --------------------------------------------------

            menu = [
                (5, "1  MESSAGES"),
                (7, "2  NODES"),
                (9, "3  STATUS"),
                (11, "4  RADIO"),
                (13, "5  SEND MESSAGE"),
                (15, "6  POWER"),
            ]

            for row, label in menu:
                self.safe_addstr(
                    stdscr,
                    row,
                    6,
                    label,
                    curses.A_BOLD,
                )

            self.safe_addstr(
                stdscr,
                16,
                6,
                "Q  QUIT",
            )

            self.draw_footer(stdscr)

            stdscr.refresh()

            # --------------------------------------------------
            # TOUCHSCREEN INPUT
            # --------------------------------------------------

            touch_point = self.touch.get_touch()

            if touch_point:
                x, y = touch_point
                self.handle_touch_menu(x, y)

            # --------------------------------------------------
            # KEYBOARD INPUT
            # --------------------------------------------------
            #
            # Some sub-screens use timeout(-1) for keyboard input.
            # Restore the short timeout whenever we return to the
            # main menu so the touchscreen keeps being polled.
            # --------------------------------------------------

            stdscr.timeout(100)
            key = stdscr.getch()

            # A touchscreen selection uses the same
            # actions as the keyboard menu.
            if self.touch_action is not None:
                touch_key = self.touch_action
                self.touch_action = None

                if touch_key == 1:
                    self.messages_screen(stdscr)

                elif touch_key == 2:
                    self.nodes_screen(stdscr)

                elif touch_key == 3:
                    self.status_screen(stdscr)

                elif touch_key == 4:
                    self.radio_screen(stdscr)

                elif touch_key == 5:
                    self.send_message_screen(stdscr)

                elif touch_key == 6:
                    self.power_screen(stdscr)

                continue

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

            elif key == ord("6"):
                self.power_screen(stdscr)

    # ------------------------------------------------------------------
    # POWER MENU
    # ------------------------------------------------------------------

    def power_screen(self, stdscr):
        """
        Safe field-node power controls.

        R = reboot
        S = shutdown
        B = back

        Touchscreen provides the same controls with large,
        deliberately separated targets.
        """

        stdscr.keypad(True)
        stdscr.timeout(100)

        while True:

            stdscr.clear()

            self.draw_header(stdscr)

            self.safe_addstr(
                stdscr,
                5,
                4,
                "POWER",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                6,
                4,
                "-" * 70,
            )

            self.safe_addstr(
                stdscr,
                8,
                4,
                "FIELD NODE POWER CONTROLS",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                10,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                11,
                4,
                "|               REBOOT                 |",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                12,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                15,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                16,
                4,
                "|              SHUT DOWN               |",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                17,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                20,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                21,
                4,
                "|                BACK                  |",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                22,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                25,
                4,
                "R  REBOOT     S  SHUT DOWN     B  BACK",
            )

            self.draw_footer(stdscr)

            stdscr.refresh()

            # ----------------------------------------------------------
            # TOUCHSCREEN
            # ----------------------------------------------------------

            touch_point = self.touch.get_touch()

            if touch_point:

                x, y = touch_point

                if x <= 650:

                    # REBOOT
                    if 170 <= y < 235:

                        if self.confirm_power_action(
                            stdscr,
                            "REBOOT THIS FIELD NODE?",
                        ):
                            self.execute_power_action("reboot")

                        continue

                    # SHUT DOWN
                    elif 285 <= y < 350:

                        if self.confirm_power_action(
                            stdscr,
                            "SHUT DOWN THIS FIELD NODE?",
                        ):
                            self.execute_power_action("shutdown")

                        continue

                    # BACK
                    elif 395 <= y < 455:

                        return

            key = stdscr.getch()

            if key in (
                ord("b"),
                ord("B"),
                27,
            ):
                return

            elif key in (
                ord("r"),
                ord("R"),
            ):

                if self.confirm_power_action(
                    stdscr,
                    "REBOOT THIS FIELD NODE?",
                ):
                    self.execute_power_action("reboot")

            elif key in (
                ord("s"),
                ord("S"),
            ):

                if self.confirm_power_action(
                    stdscr,
                    "SHUT DOWN THIS FIELD NODE?",
                ):
                    self.execute_power_action("shutdown")

    # ------------------------------------------------------------------
    # POWER CONFIRMATION
    # ------------------------------------------------------------------

    def confirm_power_action(self, stdscr, prompt):
        """
        Require an explicit YES before reboot or shutdown.

        Y = confirm
        N / ESC = cancel
        """

        stdscr.clear()

        self.draw_header(stdscr)

        self.safe_addstr(
            stdscr,
            8,
            4,
            "POWER CONFIRMATION",
            curses.A_BOLD,
        )

        self.safe_addstr(
            stdscr,
            11,
            4,
            prompt,
            curses.A_BOLD,
        )

        # ----------------------------------------------------------
        # LARGE TOUCH-FRIENDLY CONFIRMATION BUTTONS
        # ----------------------------------------------------------

        self.safe_addstr(
            stdscr,
            14,
            4,
            "+--------------------------------------+",
            curses.A_BOLD,
        )

        self.safe_addstr(
            stdscr,
            15,
            4,
            "|             YES / CONFIRM            |",
            curses.A_BOLD,
        )

        self.safe_addstr(
            stdscr,
            16,
            4,
            "+--------------------------------------+",
            curses.A_BOLD,
        )

        self.safe_addstr(
            stdscr,
            19,
            4,
            "+--------------------------------------+",
            curses.A_BOLD,
        )

        self.safe_addstr(
            stdscr,
            20,
            4,
            "|               NO / BACK              |",
            curses.A_BOLD,
        )

        self.safe_addstr(
            stdscr,
            21,
            4,
            "+--------------------------------------+",
            curses.A_BOLD,
        )

        self.safe_addstr(
            stdscr,
            24,
            4,
            "Y  YES     N  NO     ESC  CANCEL",
        )

        self.draw_footer(stdscr)

        stdscr.refresh()

        while True:

            # ------------------------------------------------------
            # TOUCHSCREEN CONFIRMATION
            # ------------------------------------------------------

            touch_point = self.touch.get_touch()

            if touch_point:

                x, y = touch_point

                if x <= 650:

                    # YES
                    if 170 <= y < 235:
                        return True

                    # NO / BACK
                    elif 285 <= y < 350:
                        return False

            key = stdscr.getch()

            if key in (
                ord("y"),
                ord("Y"),
            ):
                return True

            if key in (
                ord("n"),
                ord("N"),
                27,
            ):
                return False

    # ------------------------------------------------------------------
    # POWER ACTION
    # ------------------------------------------------------------------

    def execute_power_action(self, action):
        """
        Hand the final power operation to systemd.

        The menu process does not perform any additional UI work
        after this call because the machine is expected to transition.
        """

        import subprocess

        if action == "reboot":

            subprocess.Popen(
                [
                    "sudo",
                    "systemctl",
                    "reboot",
                ],
                start_new_session=True,
            )

        elif action == "shutdown":

            subprocess.Popen(
                [
                    "sudo",
                    "systemctl",
                    "poweroff",
                ],
                start_new_session=True,
            )

    # ------------------------------------------------------------------
    # SAFE SCREEN OUTPUT
    # ------------------------------------------------------------------

    def safe_addstr(
        self,
        stdscr,
        row,
        col,
        text,
        attributes=0,
    ):
        """Write text without allowing terminal-size errors to crash UI."""

        try:
            height, width = stdscr.getmaxyx()

            if row < 0 or row >= height:
                return

            if col < 0 or col >= width:
                return

            available = width - col

            if available <= 0:
                return

            stdscr.addstr(
                row,
                col,
                str(text)[:available],
                attributes,
            )

        except curses.error:
            pass

    # ------------------------------------------------------------------
    # HEADER / FOOTER
    # ------------------------------------------------------------------

    def draw_header(self, stdscr):
        # ------------------------------------------------------
        # FREEWAVE CRT PHOSPHOR HEADER
        # ------------------------------------------------------

        title = "FREEWAVE SIGNAL SOCIETY"
        subtitle = "CHICAGO DIVISION — FIELD NODE"

        try:
            height, width = stdscr.getmaxyx()

            title_x = max(
                0,
                (width - len(title)) // 2
            )

            subtitle_x = max(
                0,
                (width - len(subtitle)) // 2
            )

            # High-intensity phosphor effect:
            # bold + standout gives compatible terminals
            # a much stronger CRT appearance.
            crt = (
                curses.color_pair(7)
                | curses.A_BOLD
            )

            self.safe_addstr(
                stdscr,
                0,
                title_x,
                title,
                crt,
            )

            self.safe_addstr(
                stdscr,
                1,
                subtitle_x,
                subtitle,
                crt,
            )

            # Heavy CRT divider
            self.safe_addstr(
                stdscr,
                3,
                2,
                "=" * max(1, width - 4),
                crt,
            )

        except Exception:
            pass

    def draw_footer(self, stdscr):
        height, _ = stdscr.getmaxyx()

        if height < 2:
            return

        try:
            connected = self.radio.is_connected()
        except Exception:
            connected = False

        connection = (
            "CONNECTED"
            if connected
            else "DISCONNECTED"
        )

        try:
            node_count = self.radio.get_node_count()
        except Exception:
            node_count = 0

        self.safe_addstr(
            stdscr,
            height - 2,
            2,
            f"RADIO: {connection}    MESH: {node_count} NODES",
        )

    # ------------------------------------------------------------------
    # MESSAGES — LIVE MONITOR
    # ------------------------------------------------------------------

    def messages_screen(self, stdscr):
        """
        Live message monitor.

        The screen automatically refreshes every 0.5 seconds.
        No manual R key is required.

        B / ESC = back
        R        = immediate refresh
        """

        stdscr.keypad(True)

        # Do NOT block indefinitely waiting for a key.
        # This allows the display to update continuously.
        stdscr.timeout(500)

        try:
            while True:
                stdscr.erase()

                self.draw_header(stdscr)

                self.safe_addstr(
                    stdscr,
                    5,
                    4,
                    "MESSAGES — LIVE MONITOR",
                    curses.A_BOLD,
                )

                self.safe_addstr(
                    stdscr,
                    6,
                    4,
                    "-" * 70,
                )

                messages = self.radio.get_messages()

                row = 8
                height, width = stdscr.getmaxyx()

                if not messages:

                    self.safe_addstr(
                        stdscr,
                        row,
                        4,
                        "NO MESSAGES RECEIVED",
                    )

                else:

                    for message in messages:

                        if row >= height - 4:
                            break

                        timestamp = message.get(
                            "time",
                            "--:--:--",
                        )

                        direction = message.get(
                            "direction",
                            "RX",
                        )

                        if direction == "TX":
                            sender = "LOCAL"

                        else:
                            sender_id = message.get(
                                "from"
                            )

                            # Use the radio's node database when
                            # available. Fall back to the node ID.
                            sender = str(sender_id or "UNKNOWN")

                            try:
                                for node in self.radio.get_nodes():
                                    if not isinstance(node, dict):
                                        continue

                                    node_id = node.get("num")

                                    if isinstance(node_id, int):
                                        node_id = f"!{node_id:08x}"

                                    if node_id == sender_id:
                                        user = node.get("user", {}) or {}

                                        sender = (
                                            user.get("longName")
                                            or user.get("shortName")
                                            or sender
                                        )
                                        break
                            except Exception:
                                pass

                            sender = sender[:12]

                        text_msg = str(
                            message.get(
                                "text",
                                "",
                            )
                        )

                        text_msg = text_msg.replace(
                            "\n",
                            " ",
                        )

                        max_width = max(
                            20,
                            width - 28,
                        )

                        if len(text_msg) > max_width:
                            text_msg = (
                                text_msg[
                                    :max_width - 3
                                ]
                                + "..."
                            )

                        line = (
                            f"{timestamp}  "
                            f"{direction:<2}  "
                            f"{sender:<12} "
                            f"{text_msg}"
                        )

                        self.safe_addstr(
                            stdscr,
                            row,
                            4,
                            line,
                        )

                        row += 1

                # ------------------------------------------------------
                # LIVE STATUS
                # ------------------------------------------------------

                self.safe_addstr(
                    stdscr,
                    height - 4,
                    4,
                    "LIVE MONITOR   B/ESC BACK     R REFRESH",
                )

                self.draw_footer(stdscr)

                stdscr.refresh()

                # ------------------------------------------------------
                # CHECK FOR USER INPUT
                #
                # timeout(500) means getch() waits a maximum of
                # 500 milliseconds before returning -1.
                #
                # That allows the loop to redraw continuously.
                # ------------------------------------------------------

                key = stdscr.getch()

                if key in (
                    ord("b"),
                    ord("B"),
                    27,
                ):
                    return

                elif key in (
                    ord("r"),
                    ord("R"),
                ):
                    # Immediate redraw.
                    continue

                # Any other key is ignored.

        finally:
            # Restore normal blocking keyboard behavior
            # before returning to the main menu.
            stdscr.timeout(-1)

    def get_sender_name(self, node_id):
        if not node_id:
            return "UNKNOWN"

        try:
            nodes = self.radio.get_nodes()
        except Exception:
            return "UNKNOWN"

        for node in nodes:

            user = node.get(
                "user",
                {},
            )

            if user.get("id") == node_id:

                return str(
                    user.get(
                        "shortName",
                        user.get(
                            "longName",
                            node_id,
                        ),
                    )
                )[:12]

        return str(node_id)[:12]

    # ------------------------------------------------------------------
    # SEND MESSAGE
    # ------------------------------------------------------------------

    def send_message_screen(self, stdscr):
        """
        Compose a broadcast or direct Meshtastic message.

        TAB selects a destination.

        Normal letters are ALWAYS treated as message text.
        """

        message = ""
        destination = "^all"
        destination_name = "BROADCAST"

        stdscr.keypad(True)
        # Poll periodically so the touchscreen remains responsive
        # while the Bluetooth keyboard is available for text entry.
        stdscr.timeout(100)

        while True:

            stdscr.clear()

            self.draw_header(stdscr)

            self.safe_addstr(
                stdscr,
                5,
                4,
                "SEND MESSAGE",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                6,
                4,
                "-" * 70,
            )

            self.safe_addstr(
                stdscr,
                8,
                4,
                f"DESTINATION: {destination_name}",
            )

            self.safe_addstr(
                stdscr,
                9,
                4,
                f"NODE ID:     {destination}",
            )

            self.safe_addstr(
                stdscr,
                11,
                4,
                "MESSAGE:",
                curses.A_BOLD,
            )

            # ----------------------------------------------------------
            # LARGE TOUCH-FRIENDLY CONTROLS
            # ----------------------------------------------------------
            #
            # These are deliberately large and widely separated.
            # The Bluetooth keyboard remains the primary text-entry
            # device.
            #
            # SELECT NODE: Y 225-285
            # SEND:        Y 300-365
            # BACK:        Y 390-445
            #
            # The visible buttons match those touch zones.
            # ----------------------------------------------------------

            self.safe_addstr(
                stdscr,
                12,
                4,
                "> " + message,
            )

            # ----------------------------------------------------------
            # LARGE VISIBLE TOUCH BUTTONS
            # ----------------------------------------------------------

            self.safe_addstr(
                stdscr,
                15,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )
            self.safe_addstr(
                stdscr,
                16,
                4,
                "|            SELECT NODE               |",
                curses.A_BOLD,
            )
            self.safe_addstr(
                stdscr,
                17,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                19,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )
            self.safe_addstr(
                stdscr,
                20,
                4,
                "|            SEND MESSAGE              |",
                curses.A_BOLD,
            )
            self.safe_addstr(
                stdscr,
                21,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                23,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )
            self.safe_addstr(
                stdscr,
                24,
                4,
                "|                 BACK                 |",
                curses.A_BOLD,
            )
            self.safe_addstr(
                stdscr,
                25,
                4,
                "+--------------------------------------+",
                curses.A_BOLD,
            )

            height, _ = stdscr.getmaxyx()

            self.safe_addstr(
                stdscr,
                height - 4,
                4,
                "KEYBOARD: TYPE MESSAGE     ENTER: SEND     ESC: CANCEL",
            )

            self.draw_footer(stdscr)

            stdscr.refresh()

            # ----------------------------------------------------------
            # TOUCHSCREEN CONTROLS
            # ----------------------------------------------------------
            #
            # Large, separated touch targets.
            #
            # SELECT NODE: Y 225-285
            # SEND:        Y 300-365
            # BACK:        Y 390-445
            #
            # Empty space between them intentionally does nothing.
            # ----------------------------------------------------------

            touch_point = self.touch.get_touch()

            if touch_point:

                x, y = touch_point

                if x <= 650:

                    # SELECT NODE
                    if 225 <= y < 285:

                        selected = self.select_destination(
                            stdscr
                        )

                        if selected is not None:
                            destination, destination_name = selected

                        continue

                    # SEND MESSAGE
                    elif 300 <= y < 365:

                        # Never send an empty message.
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

                    # BACK
                    elif 390 <= y < 445:

                        return

            try:
                cursor_x = min(
                    6 + len(message),
                    stdscr.getmaxyx()[1] - 1,
                )

                stdscr.move(
                    12,
                    cursor_x,
                )

            except curses.error:
                pass

            key = stdscr.getch()

            # ----------------------------------------------------------
            # ESC = CANCEL
            # ----------------------------------------------------------

            if key == 27:
                return

            # ----------------------------------------------------------
            # TAB = NODE SELECTOR
            # ----------------------------------------------------------

            if key == 9:

                selected = self.select_destination(
                    stdscr
                )

                if selected is not None:
                    destination, destination_name = selected

                continue

            # ----------------------------------------------------------
            # BACKSPACE
            # ----------------------------------------------------------

            if key in (
                curses.KEY_BACKSPACE,
                127,
                8,
            ):

                message = message[:-1]

                continue

            # ----------------------------------------------------------
            # ENTER = SEND
            # ----------------------------------------------------------

            if key in (
                curses.KEY_ENTER,
                10,
                13,
            ):

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

            # ----------------------------------------------------------
            # PRINTABLE CHARACTERS
            #
            # N IS SAFE.
            # R IS SAFE.
            # Q IS SAFE.
            # B IS SAFE.
            # ----------------------------------------------------------

            if 32 <= key <= 126:

                if len(message) < 200:

                    message += chr(key)

    # ------------------------------------------------------------------
    # DESTINATION SELECTOR
    # ------------------------------------------------------------------

    def select_destination(self, stdscr):

        stdscr.keypad(True)
        stdscr.timeout(-1)

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

            user = node.get(
                "user",
                {},
            )

            node_id = user.get("id")

            if not node_id:
                continue

            # Never offer our own node.
            if node_id == self.radio.get_node_id():
                continue

            entries.append(
                {
                    "id": node_id,
                    "short": user.get(
                        "shortName",
                        "----",
                    ),
                    "long": user.get(
                        "longName",
                        node_id,
                    ),
                    "num": node.get("num"),
                }
            )

        selected = 0
        top = 0

        while True:

            stdscr.clear()

            self.draw_header(stdscr)

            self.safe_addstr(
                stdscr,
                5,
                4,
                "SELECT DESTINATION",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                6,
                4,
                "-" * 70,
            )

            self.safe_addstr(
                stdscr,
                7,
                4,
                "UP/DOWN or J/K  SELECT     ENTER  CHOOSE     ESC  CANCEL",
            )

            height, width = stdscr.getmaxyx()

            visible_rows = max(
                5,
                height - 12,
            )

            if selected < top:
                top = selected

            if selected >= top + visible_rows:
                top = (
                    selected
                    - visible_rows
                    + 1
                )

            visible_entries = range(
                top,
                min(
                    len(entries),
                    top + visible_rows,
                ),
            )

            for screen_row, index in enumerate(
                visible_entries
            ):

                entry = entries[index]

                prefix = (
                    ">"
                    if index == selected
                    else " "
                )

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
                    f"{prefix} "
                    f"{short_name:<8} "
                    f"{long_name:<32} "
                    f"{node_id}"
                )

                attributes = (
                    curses.A_REVERSE
                    if index == selected
                    else 0
                )

                self.safe_addstr(
                    stdscr,
                    9 + screen_row,
                    4,
                    line[
                        :max(
                            20,
                            width - 8,
                        )
                    ],
                    attributes,
                )

            self.safe_addstr(
                stdscr,
                height - 5,
                4,
                f"AVAILABLE DESTINATIONS: {len(entries)}",
            )

            self.draw_footer(stdscr)

            stdscr.refresh()

            key = stdscr.getch()

            if key == 27:
                return None

            elif key in (
                curses.KEY_UP,
                ord("k"),
                ord("K"),
            ):

                selected = max(
                    0,
                    selected - 1,
                )

            elif key in (
                curses.KEY_DOWN,
                ord("j"),
                ord("J"),
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
                    (
                        entry["short"]
                        if entry["id"] != "^all"
                        else "BROADCAST"
                    ),
                )

    # ------------------------------------------------------------------
    # ERROR DISPLAY
    # ------------------------------------------------------------------

    def show_error(self, stdscr, text):

        height, _ = stdscr.getmaxyx()

        self.safe_addstr(
            stdscr,
            height - 5,
            4,
            text,
        )

        self.safe_addstr(
            stdscr,
            height - 4,
            4,
            "PRESS ANY KEY",
        )

        stdscr.refresh()

        stdscr.getch()

    # ------------------------------------------------------------------
    # NODES
    # ------------------------------------------------------------------

    def nodes_screen(self, stdscr):

        stdscr.keypad(True)
        stdscr.timeout(-1)

        while True:

            stdscr.clear()

            self.draw_header(stdscr)

            self.safe_addstr(
                stdscr,
                5,
                4,
                "NODES",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                6,
                4,
                "-" * 70,
            )

            nodes = self.radio.get_nodes()

            row = 8

            height, width = stdscr.getmaxyx()

            for node in nodes:

                if row >= height - 4:
                    break

                user = node.get(
                    "user",
                    {},
                )

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

                line = (
                    f"{str(short_name)[:8]:<8} "
                    f"{str(name)[:28]:<28} "
                    f"{node_id}"
                )

                self.safe_addstr(
                    stdscr,
                    row,
                    4,
                    line,
                )

                row += 1

            self.draw_footer(stdscr)

            self.safe_addstr(
                stdscr,
                height - 3,
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

            elif key in (
                ord("r"),
                ord("R"),
            ):
                continue

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def status_screen(self, stdscr):

        stdscr.keypad(True)
        stdscr.timeout(-1)

        while True:

            stdscr.clear()

            self.draw_header(stdscr)

            self.safe_addstr(
                stdscr,
                5,
                4,
                "SYSTEM STATUS",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                6,
                4,
                "-" * 70,
            )

            try:
                cpu_temp = get_cpu_temperature()
            except Exception:
                cpu_temp = "N/A"

            try:
                memory = get_memory()
            except Exception:
                memory = "N/A"

            try:
                uptime = format_uptime(
                    get_uptime()
                )
            except Exception:
                uptime = "N/A"

            self.safe_addstr(
                stdscr,
                9,
                4,
                f"CPU TEMPERATURE: {cpu_temp}",
            )

            self.safe_addstr(
                stdscr,
                11,
                4,
                f"MEMORY:          {memory}",
            )

            self.safe_addstr(
                stdscr,
                13,
                4,
                f"UPTIME:           {uptime}",
            )

            self.draw_footer(stdscr)

            height, _ = stdscr.getmaxyx()

            self.safe_addstr(
                stdscr,
                height - 3,
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

            elif key in (
                ord("r"),
                ord("R"),
            ):
                continue

    # ------------------------------------------------------------------
    # RADIO
    # ------------------------------------------------------------------

    def radio_screen(self, stdscr):

        stdscr.keypad(True)
        stdscr.timeout(-1)

        while True:

            stdscr.clear()

            self.draw_header(stdscr)

            self.safe_addstr(
                stdscr,
                5,
                4,
                "RADIO STATUS",
                curses.A_BOLD,
            )

            self.safe_addstr(
                stdscr,
                6,
                4,
                "-" * 70,
            )

            try:
                connected = self.radio.is_connected()
            except Exception:
                connected = False

            connection = (
                "CONNECTED"
                if connected
                else "DISCONNECTED"
            )

            node_id = self.radio.get_node_id()
            node_count = self.radio.get_node_count()
            info = self.radio.get_local_info()

            self.safe_addstr(
                stdscr,
                9,
                4,
                f"RADIO:             {connection}",
            )

            self.safe_addstr(
                stdscr,
                11,
                4,
                f"LOCAL NODE:        {node_id or 'UNKNOWN'}",
            )

            self.safe_addstr(
                stdscr,
                13,
                4,
                f"MESH NODES:        {node_count}",
            )

            self.safe_addstr(
                stdscr,
                15,
                4,
                f"LONG NAME:         {info.get('long_name', 'Unknown')}",
            )

            self.safe_addstr(
                stdscr,
                16,
                4,
                f"SHORT NAME:        {info.get('short_name', 'Unknown')}",
            )

            self.safe_addstr(
                stdscr,
                17,
                4,
                f"HARDWARE:          {info.get('hardware', 'Unknown')}",
            )

            battery = info.get("battery")
            voltage = info.get("voltage")

            if battery is not None:

                self.safe_addstr(
                    stdscr,
                    19,
                    4,
                    f"BATTERY:           {battery}%",
                )

            if voltage is not None:

                self.safe_addstr(
                    stdscr,
                    20,
                    4,
                    f"VOLTAGE:           {voltage} V",
                )

            self.draw_footer(stdscr)

            height, _ = stdscr.getmaxyx()

            self.safe_addstr(
                stdscr,
                height - 3,
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

            elif key in (
                ord("r"),
                ord("R"),
            ):
                continue
