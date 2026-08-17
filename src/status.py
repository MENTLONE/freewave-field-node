import os
import time


def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read().strip()) / 1000.0
    except Exception:
        return None


def get_memory():
    try:
        with open("/proc/meminfo", "r") as f:
            values = {}

            for line in f:
                parts = line.split()

                if len(parts) >= 2:
                    key = parts[0].rstrip(":")
                    values[key] = int(parts[1])

        total = values.get("MemTotal", 0)
        available = values.get("MemAvailable", 0)

        used = total - available

        return {
            "total": total // 1024,
            "used": used // 1024,
            "available": available // 1024,
        }

    except Exception:
        return {}


def get_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            seconds = float(f.readline().split()[0])

        return int(seconds)

    except Exception:
        return 0


def format_uptime(seconds):
    days = seconds // 86400
    seconds %= 86400

    hours = seconds // 3600
    seconds %= 3600

    minutes = seconds // 60

    return f"{days}d {hours:02d}h {minutes:02d}m"
