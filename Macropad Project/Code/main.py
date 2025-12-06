import board
import time

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.rgb import RGB

keyboard = KMKKeyboard()

# --- MACROS ---
macros = Macros()
keyboard.modules.append(macros)

# --- LED SETUP (SK6812MINI) ---
rgb = RGB(
    pixel_pin=board.SDA,   # Your GPIO6/SDA pin
    num_pixels=2,          # You have 2 LEDs daisy-chained
    val_limit=100,
)
keyboard.modules.append(rgb)

# Turn on power LED (LED 0 = green)
def set_power_led():
    rgb.pixels[0] = (0, 255, 0)   # Green
    rgb.show()

set_power_led()

# Flash LED 1 red
def flash_key_led():
    rgb.pixels[1] = (255, 0, 0)   # Red
    rgb.show()
    time.sleep(0.1)               # 100ms flash
    rgb.pixels[1] = (0, 0, 0)     # Off
    rgb.show()

# --- KEY PINS ---
PINS = [board.D3, board.D4, board.D2, board.D1, board.D7, board.D0]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# --- KEYMAP ---
keyboard.keymap = [
    [
        KC.Macro(Press(KC.LCTRL), Tap(KC.C), Release(KC.LCTRL)),
        KC.Macro(Press(KC.LCTRL), Tap(KC.V), Release(KC.LCTRL)),
        KC.Macro(Press(KC.LCTRL), Tap(KC.Z), Release(KC.LCTRL)),
        KC.Macro(Press(KC.LCTRL), Tap(KC.S), Release(KC.LCTRL)),
        KC.Macro("jonahjgregory@gmail.com"),
        KC.Macro(Press(KC.LCTRL), Press(KC.LSHIFT), Press(KC.ESC), Release(KC.ESC), Release(KC.LSHIFT), Release(KC.LCTRL)),
    ]
]

# --- Add keypress hook ---
last_state = keyboard.matrix.get_state()

def on_keypress():
    flash_key_led()

keyboard.before_matrix_scan = lambda: None

def check_keys():
    global last_state
    new_state = keyboard.matrix.get_state()

    if new_state != last_state:     # a key state changed
        if True in new_state:       # a key is pressed
            on_keypress()

    last_state = new_state

keyboard.before_matrix_scan = check_keys

# --- START KMK ---
if __name__ == '__main__':
    keyboard.go()
