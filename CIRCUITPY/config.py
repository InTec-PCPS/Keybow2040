#Basic USB-HID setup
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

#Basic MIDI setup
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

from macro_handler import MacroHandler
macro_comm = MacroHandler()

# Configuration options
BRIGHTNESS = 0.25  # NeoPixel and LED brightness
INACTIVITY_TIMEOUT = 30  # OLED sleep timeout in seconds

# Character Map with Platform Support (adafruit_hid only supports US layout; macro_handler can use UTF-16)
# These are Spanish-specific, but other sections could be added for other languages.
def spanish_char(char, platform="WIN"):
    utf_map = {
        'ñ': {"MAC": ("UTF16", "MAC", "00F1"), "WIN": ("UTF16", "WIN", "00F1"), "NIX": ("UTF16", "NIX", "00F1")},
        'Ñ': {"MAC": ("UTF16", "MAC", "00D1"), "WIN": ("UTF16", "WIN", "00D1"), "NIX": ("UTF16", "NIX", "00D1")},
        'á': {"MAC": ("UTF16", "MAC", "00E1"), "WIN": ("UTF16", "WIN", "00E1"), "NIX": ("UTF16", "NIX", "00E1")},
        'Á': {"MAC": ("UTF16", "MAC", "00C1"), "WIN": ("UTF16", "WIN", "00C1"), "NIX": ("UTF16", "NIX", "00C1")},
        'é': {"MAC": ("UTF16", "MAC", "00E9"), "WIN": ("UTF16", "WIN", "00E9"), "NIX": ("UTF16", "NIX", "00E9")},
        'É': {"MAC": ("UTF16", "MAC", "00C9"), "WIN": ("UTF16", "WIN", "00C9"), "NIX": ("UTF16", "NIX", "00C9")},
        'í': {"MAC": ("UTF16", "MAC", "00ED"), "WIN": ("UTF16", "WIN", "00ED"), "NIX": ("UTF16", "NIX", "00ED")},
        'Í': {"MAC": ("UTF16", "MAC", "00CD"), "WIN": ("UTF16", "WIN", "00CD"), "NIX": ("UTF16", "NIX", "00CD")},
        'ó': {"MAC": ("UTF16", "MAC", "00F3"), "WIN": ("UTF16", "WIN", "00F3"), "NIX": ("UTF16", "NIX", "00F3")},
        'Ó': {"MAC": ("UTF16", "MAC", "00D3"), "WIN": ("UTF16", "WIN", "00D3"), "NIX": ("UTF16", "NIX", "00D3")},
        'ú': {"MAC": ("UTF16", "MAC", "00FA"), "WIN": ("UTF16", "WIN", "00FA"), "NIX": ("UTF16", "NIX", "00FA")},
        'Ú': {"MAC": ("UTF16", "MAC", "00DA"), "WIN": ("UTF16", "WIN", "00DA"), "NIX": ("UTF16", "NIX", "00DA")},
        'ü': {"MAC": ("UTF16", "MAC", "00FC"), "WIN": ("UTF16", "WIN", "00FC"), "NIX": ("UTF16", "NIX", "00FC")},
        'Ü': {"MAC": ("UTF16", "MAC", "00DC"), "WIN": ("UTF16", "WIN", "00DC"), "NIX": ("UTF16", "NIX", "00DC")},
        '¡': {"MAC": ("UTF16", "MAC", "00A1"), "WIN": ("UTF16", "WIN", "00A1"), "NIX": ("UTF16", "NIX", "00A1")},
        '¿': {"MAC": ("UTF16", "MAC", "00BF"), "WIN": ("UTF16", "WIN", "00BF"), "NIX": ("UTF16", "NIX", "00BF")},
    }
    return utf_map.get(char, {}).get(platform, ("KEY", Keycode.SPACE))

# Layer Colors
colours = {
    0: (int(255 * BRIGHTNESS), 0, int(255 * BRIGHTNESS)),  # Purple
    1: (0, int(255 * BRIGHTNESS), int(255 * BRIGHTNESS)),  # Cyan
    2: (int(255 * BRIGHTNESS), int(255 * BRIGHTNESS), 0),  # Yellow
    3: (int(128 * BRIGHTNESS), int(128 * BRIGHTNESS), int(128 * BRIGHTNESS)), #Gray
}

# Define the layers. Supports key, text, media, mouse, and midi.
# Keybow2040 numbers from 0 at bottom left and continues bottom-to-top and left-to-right to 15 at top right.
layers = {
    0: {
        3: ("KEY", Keycode.SEVEN), 7: ("KEY", Keycode.EIGHT), 11: ("KEY", Keycode.NINE), 15: ("KEY", Keycode.KEYPAD_ASTERISK),
        2: ("KEY", Keycode.FOUR), 6: ("KEY", Keycode.FIVE), 10: ("KEY", Keycode.SIX), 14: ("KEY", Keycode.KEYPAD_MINUS),
        1: ("KEY", Keycode.ONE), 5: ("KEY", Keycode.TWO), 9: ("KEY", Keycode.THREE), 13: ("KEY", Keycode.KEYPAD_PLUS),
        0: ("KEY", Keycode.ZERO), 4: ("KEY", Keycode.KEYPAD_PERIOD), 8: ("KEY", Keycode.DELETE),12: ("KEY", Keycode.ENTER)
        },
    1: {
        3: ("TEXT", " lang=\"es\""),
        2: ("TEXT", "<strong>"), 6: ("TEXT", "</strong>"),
        1: ("TEXT", "<span lang=\"es\">"), 5: ("TEXT", "</span>"),
        0: ("TEXT", " target=\"_blank\"")
        },
    2: {
        3: spanish_char('á', platform="WIN"), 7: spanish_char('Á', platform="WIN"), 11: spanish_char('ú', platform="WIN"), 15: spanish_char('Ú', platform="WIN"),
        2: spanish_char('é', platform="WIN"), 6: spanish_char('É', platform="WIN"), 10: spanish_char('ü', platform="WIN"), 14: spanish_char('Ü', platform="WIN"),
        1: spanish_char('í', platform="WIN"), 5: spanish_char('Í', platform="WIN"), 9: spanish_char('ñ', platform="WIN"), 13: spanish_char('Ñ', platform="WIN"),
        0: spanish_char('ó', platform="WIN"), 4: spanish_char('Ó', platform="WIN"), 8: spanish_char('¿', platform="WIN"), 12: spanish_char('¡', platform="WIN")
        },
    3: {
        3: ("KEY", Keycode.SPACE),
        2: ("KEY", Keycode.T), 6: ("MIDI", ControlChange(7, 100)),  # Control Change for volume control, value 100
        1: ("KEY", Keycode.D), 5: ("MIDI", NoteOff(60, 0)),     # Send NoteOff for middle C
        0: ("KEY", Keycode.X), 4: ("MIDI", NoteOn(60, 120))   # Send NoteOn for middle C with velocity 120
        }
}

# Layer Labels for OLED Display
# Keybow2040 numbers from 0 at bottom left and continues bottom-to-top and left-to-right to 15 at top right.
layer_labels_map = {
    0: {
        3: "7", 7: "8", 11: "9", 15: "*",
        2: "4", 6: "5", 10: "6", 14: "-",
        1: "1", 5: "2", 9: "3", 13: "+",
        0: "0", 4: ".", 8: "Del", 12: "Enter",
        },
    1: {
        3: "LNG",
        2: "STR", 6: "/STR",
        1: "<LNG>", 5: "</LNG>",
        0: "TGT"
        },
    2: {
        3: "'a", 7: "'A", 11: "'u", 15: "'U",
        2: "'e", 6: "'E", 10: ":u", 14: ":U",
        1: "'i", 5: "'I", 9: "~n", 13: "~N",
        0: "'o", 4: "'O", 8: "?", 12: "!"
        },
    3: {
        3: "Space",
        2: "T", 6: "CCvol",
        1: "D", 5: "C4off",
        0: "X", 4: "C4on"
        }
}

# Encoder actions per layer, defined separately from layers. Default is volume-up and volume-down.
encoder_actions = {
    0: {
        "encoder-up": lambda: print("Layer 1 Encoder Up"),
        "encoder-down": lambda: print("Layer 1 Encoder Down")
        },
    1: {
        "encoder-up": lambda: print("Layer 1 Encoder Up"),
        "encoder-down": lambda: print("Layer 1 Encoder Down")
        },
    2: {
        "encoder-up": lambda: print("Layer 2 Encoder Up"),
        "encoder-down": lambda: print("Layer 2 Encoder Down")
        },
    3: {
        "encoder-up": lambda: print("Layer 3 Encoder Up"),
        "encoder-down": lambda: print("Layer 3 Encoder Down")
        },
}

# Definitions for large, "7-segment" style graphics for layer indication
numbers_bitmap = {
    '0': [
        "111",
        "101",
        "101",
        "101",
        "111",
    ],
    '1': [
        "110",
        "010",
        "010",
        "010",
        "111",
    ],
    '2': [
        "111",
        "001",
        "111",
        "100",
        "111",
    ],
    '3': [
        "111",
        "001",
        "111",
        "001",
        "111",
    ],
    '4': [
        "101",
        "101",
        "111",
        "001",
        "001",
    ],
}