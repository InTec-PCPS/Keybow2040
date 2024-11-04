# Keybow2040
A macropad built around Pimoroni's Keybow2040 with OLED and rotary encoder. This is a personal project that I use daily. It works, so I thought I'd share.
* Works with CircuitPython 9.2.0
* Supports keypresses, text macros, and non-US characters. Should also support mouse and MIDI events, but untested so far.
* Multiple types can be used in each layer...and even chained in a single macro.
* Press encoder to change layers. Displays a large bitmapped number on layer changes.
* Encoder up/down actions are configurable per layer, but volume up/down is the default if nothing else is set. Still testing this.
* Set up for four layers (0-3) by default, but more can be added.
* Configuration is separate from the code.py that runs the thing. Makes it harder for me to mess up.
## Credits
* Original Idea and 3D-printed case files: [ManelTo](https://www.printables.com/model/228327-keybow2040-macropad-with-display-and-encoder)
* Updated ideas and instructions: [ntindle](https://github.com/ntindle/Keybow2040-Macro-Pad/tree/main)
* PMK library and HID examples: [Pimoroni](https://github.com/pimoroni/pmk-circuitpython)
* Macro-Handler: [Nox Ferocia](https://forums.pimoroni.com/t/macro-handler-for-keybow2040-pico-keypad-base-etc/21080)
  * This goldmine gives macro chaining, multiple types per layer, and non-US character support.
* Devs who created the adafruit bundle and PMK library.
## Image
![macropad with oled and rotary encoder](https://github.com/InTec-PCPS/Keybow2040/blob/main/layer0.jpg?raw=true)
I guess the refresh rate of the OLED display doesn't mesh with my camera. There IS another row at the top.
## Parts Used
* [Pimoroni Keybow2040](https://shop.pimoroni.com/products/keybow-2040?variant=32399559589971)
* [Adafruit I2C OLED Module](https://www.adafruit.com/product/326)
* [Adafruit Rotary Encoder Module](https://www.adafruit.com/product/4991)
* [Adafruit STEMMA QT cables](https://www.adafruit.com/product/4399) I used a 50mm QT-to-QT cable and a 100mm QT-to-bare wire cable.
## Other Parts
* 3D-printed case designed by ManelTo
* M2.5 heat-set inserts
* Soldering iron
* Aa box of M2.5 screws in various lenghts, sold as a laptop screw kit.
* Keycaps (extra nuphy keys) and a generic knob.
## Process
1. Printed case files and inserted heat-set inserts, per ntindle's instructions.
2. Soldered QT cable to the keybow2040. Four wires: +3V, GND, SDA, SCL.
3. Mounted keybow2040, OLED, and encoder board in case with M2.5 screws. Assembled case.
4. Flashed CircuitPython UF2 (version 9.2 RC on mine)
5. Lots of trial and error.
6. Working code provided here.
## Still working on...
* Testing MIDI support
* Testing encoder actions per layer
* Testing mouse events
