# SPDX-FileCopyrightText: Copyright (C) 2025 ARDUINO SA <http://www.arduino.cc>
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import Logger, Bridge

logger = Logger(__name__)

LED_IDS = [1, 2, 3, 4]  # Supported LED IDs

LED_BRIGHTNESS_FILES = [
    "/sys/class/leds/red:user/brightness",
    "/sys/class/leds/green:user/brightness",
    "/sys/class/leds/blue:user/brightness",
    "/sys/class/leds/red:panic/brightness",
    "/sys/class/leds/green:wlan/brightness",
    "/sys/class/leds/blue:bt/brightness",
]


def write_led_file(led_file, color):
    try:
        with open(led_file, "w") as f:
            f.write(f"{color}\n")
    except Exception as e:
        print(f"Error writing to {led_file}: {e}")


class Leds:
    @staticmethod
    # Led 1 and 2 are controlled by directly (MPU), while Led 3 and 4 are controlled via Bridge (MCU)
    def set_led_color(ledid: int, rgb_color: dict):
        try:
            if ledid not in LED_IDS:
                raise ValueError(f"Unknown led '{ledid}'")

            if not rgb_color or not all(k in rgb_color for k in ("r", "g", "b")):
                raise ValueError("Color must be an object with 'r', 'g', 'b' keys")

            match ledid:
                case 1:
                    Leds.set_led1_color(rgb_color["r"], rgb_color["g"], rgb_color["b"])
                case 2:
                    Leds.set_led2_color(rgb_color["r"], rgb_color["g"], rgb_color["b"])
                case 3:
                    Leds.set_led3_color(rgb_color["r"], rgb_color["g"], rgb_color["b"])
                case 4:
                    Leds.set_led4_color(rgb_color["r"], rgb_color["g"], rgb_color["b"])

        except Exception as e:
            Logger(__name__).error(f"LED color set error: {e}")

    @staticmethod
    def set_led1_color(r, g, b):
        write_led_file(LED_BRIGHTNESS_FILES[0], r)
        write_led_file(LED_BRIGHTNESS_FILES[1], g)
        write_led_file(LED_BRIGHTNESS_FILES[2], b)

    @staticmethod
    def set_led2_color(r, g, b):
        write_led_file(LED_BRIGHTNESS_FILES[3], r)
        write_led_file(LED_BRIGHTNESS_FILES[4], g)
        write_led_file(LED_BRIGHTNESS_FILES[5], b)

    def set_led3_color(r, g, b):
        Bridge.call("set_led_color", 3, r, g, b)

    def set_led4_color(r, g, b):
        Bridge.call("set_led_color", 4, r, g, b)
