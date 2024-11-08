#Import libraries for keys and LEDs. MacroHandler gets the HID libraries.
import time
from pmk import PMK
from pmk.platform.keybow2040 import Keybow2040 as Hardware
from macro_handler import MacroHandler

#Import libraries to support the OLED module
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C

#Import libraries to support the rotary encoder module
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.rotaryio import IncrementalEncoder
from adafruit_seesaw.neopixel import NeoPixel

#Import libraries to support MIDI events
import usb_midi
from adafruit_midi import MIDI

# Import custom configuration from config.py which contains all the editable bits.
from config import (
    BRIGHTNESS,
    INACTIVITY_TIMEOUT,
    colours,
    layers,
    encoder_actions,
    layer_labels_map,
    spanish_char,
    numbers_bitmap
)
print("\n[OK] Libraries and configuration")

# Start up the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
print("[OK] I2C bus")

# Scan the I2C bus to confirm device addresses
while not i2c.try_lock():
    pass
try:
    addresses = [hex(device_address) for device_address in i2c.scan()]
    print("     I2C addresses found:", addresses)
finally:
    i2c.unlock()

# Start up the OLED module
oled = SSD1306_I2C(128, 64, i2c, addr=0x3D)
oled.fill(0)
oled.text("Display Ready", 0, 0, 1)
oled.show()
print("[OK] OLED display")
time.sleep(2)

# Initialize Keybow and MacroHandler
keybow = PMK(Hardware(i2c=i2c))
keys = keybow.keys
macro_comm = MacroHandler()
print("[OK] Keybow and MacroHandler")

# Initialize Rotary Encoder and NeoPixel on Seesaw
encoder = Seesaw(i2c, addr=0x36)
encoder_button = DigitalIO(encoder, 24)
rotary_encoder = IncrementalEncoder(encoder)
last_position = rotary_encoder.position
neopixel = NeoPixel(encoder, 6, 1, brightness=BRIGHTNESS)
print("[OK] Rotary encoder and NeoPixel")

# Initialize MIDI on USB
midi = MIDI(midi_out=usb_midi.ports[1], out_channel=1)
print("[OK] USB MIDI on MIDI channel 1")

current_layer = 0
last_activity_time = time.monotonic()
oled_active = True

# Display large layer number on changes
def display_large_layer_text(layer):
    oled.fill(0)
    text = str(layer)

    # Define pixel size and spacing for each block
    pixel_size = 8
    x_offset = 48  # Adjust to center the number horizontally
    y_offset = 16  # Adjust to center vertically

    if text in numbers_bitmap:
        bitmap = numbers_bitmap[text]
        
        for row, line in enumerate(bitmap):
            for col, pixel in enumerate(line):
                if pixel == "1":
                    x = x_offset + col * pixel_size
                    y = y_offset + row * pixel_size
                    oled.fill_rect(x, y, pixel_size, pixel_size, 1)

    oled.show()
    time.sleep(1)

# Display Key Labels on OLED
def update_oled_layer_display(layer):
    display_large_layer_text(layer)
    oled.fill(0)
    oled.show()
    layer_labels = layer_labels_map.get(layer, {i: "" for i in range(16)})
    for col in range(4):
        for row in range(4):
            key_index = col * 4 + (3 - row)
            label_text = layer_labels.get(key_index, "")
            oled.text(label_text, col * 32, row * 16, 1)  # (for 128x64)
    oled.show()

def sleep_oled():
    global oled_active
    oled.fill(0)
    oled.show()
    oled_active = False
    print("OLED is very sleepy.")

def wake_oled():
    global oled_active
    if not oled_active:
        update_oled_layer_display(current_layer)

def update_leds_for_layer(layer):
    for k in range(16):
        keys[k].set_led(0, 0, 0)
    for k in layers[layer].keys():
        keys[k].set_led(*colours[layer])
    neopixel.fill(colours[layer])

# Sets the initial LED and OLED display for Layer 0
update_oled_layer_display(current_layer)
update_leds_for_layer(current_layer)

# Main Loop
print("[OK] All good. Starting Main Loop.")
while True:
    keybow.update()
    current_time = time.monotonic()

   # Check for encoder rotation
    position = rotary_encoder.position
    if position > last_position:  # Encoder rotated up
        # Check if current layer has an 'encoder-up' action defined
        if current_layer in encoder_actions and "encoder-up" in encoder_actions[current_layer]:
            encoder_actions[current_layer]["encoder-up"]()  # Execute layer-specific up action
        else:
            macro_comm.send_macro(("MEDIA", ConsumerControlCode.VOLUME_INCREMENT))  # Default to volume up
        last_position = position

    elif position < last_position:  # Encoder rotated down
        # Check if current layer has an 'encoder-down' action defined
        if current_layer in encoder_actions and "encoder-down" in encoder_actions[current_layer]:
            encoder_actions[current_layer]["encoder-down"]()  # Execute layer-specific down action
        else:
            macro_comm.send_macro(("MEDIA", ConsumerControlCode.VOLUME_DECREMENT))  # Default to volume down
        last_position = position


    # Encoder button press handling for layer switching...
    if not encoder_button.value:
        current_layer = (current_layer + 1) % len(layers)
        update_oled_layer_display(current_layer)
        update_leds_for_layer(current_layer)


    # Keypress handler
    for k in layers[current_layer].keys():
        if keys[k].pressed:
            wake_oled()  # Wake OLED on activity
            last_activity_time = current_time
            print(f"Key {k} pressed in Layer {current_layer}")
            macro_type, macro_data = layers[current_layer][k]

            # Check macro type to handle MIDI separately
            if macro_type == "MIDI":
                midi.send(macro_data)
            else:
                macro_comm.send_macro((macro_type, macro_data))

    # Check for OLED sleep mode
    if oled_active and (current_time - last_activity_time > INACTIVITY_TIMEOUT):
        sleep_oled()
