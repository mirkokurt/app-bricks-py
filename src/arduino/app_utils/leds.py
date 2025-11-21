# SPDX-FileCopyrightText: Copyright (C) 2025 ARDUINO SA <http://www.arduino.cc>
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import Logger

logger = Logger(__name__)


class Leds:
    _led_ids = [1, 2]  # Supported LED IDs (Led 3 and 4 can't be controlled directly by MPU but only by MCU via Bridge)

    _led1_brightness_files = [
        "/sys/class/leds/red:user/brightness",
        "/sys/class/leds/green:user/brightness",
        "/sys/class/leds/blue:user/brightness",
    ]
    _led2_brightness_files = [
        "/sys/class/leds/red:panic/brightness",
        "/sys/class/leds/green:wlan/brightness",
        "/sys/class/leds/blue:bt/brightness",
    ]

    @staticmethod
    def _write_led_file(led_file, value: bool):
        try:
            with open(led_file, "w") as f:
                f.write(f"{int(value)}\n")
        except Exception as e:
            print(f"Error writing to {led_file}: {e}")

    @staticmethod
    def set_led1_color(r: bool, g: bool, b: bool):
        Leds._write_led_file(Leds._led1_brightness_files[0], r)
        Leds._write_led_file(Leds._led1_brightness_files[1], g)
        Leds._write_led_file(Leds._led1_brightness_files[2], b)

    @staticmethod
    def set_led2_color(r: bool, g: bool, b: bool):
        Leds._write_led_file(Leds._led2_brightness_files[0], r)
        Leds._write_led_file(Leds._led2_brightness_files[1], g)
        Leds._write_led_file(Leds._led2_brightness_files[2], b)
