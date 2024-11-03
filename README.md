# Keybow2040
A macropod built around Pimoroni's Keybow2040 with OLED and rotary encoder.
Works with CircuitPython 9.x
Supports MIDI events. Also supports key, text, and mouse events, plus non-US keyboard characters.
## Credits
* Original Idea and 3D-printed case files: [ManelTo](https://www.printables.com/model/228327-keybow2040-macropad-with-display-and-encoder)
* Updated firmware: [ntindle](https://github.com/ntindle/Keybow2040-Macro-Pad/tree/main)
* Macro-Handler: [Nox Ferocia](https://forums.pimoroni.com/t/macro-handler-for-keybow2040-pico-keypad-base-etc/21080)
* Devs who created the adafruit bundle and PMK library.
## Image
![macropad with oled and rotary encoder](https://github.com/InTec-PCPS/Keybow2040/blob/main/layer0.jpg?raw=true)
## Parts Used
* [Pimoroni Keybow2040](https://shop.pimoroni.com/products/keybow-2040?variant=32399559589971)
* [Adafruit I2C OLED Module](https://www.adafruit.com/product/326)
* [Adafruit Rotary Encoder Module](https://www.adafruit.com/product/4991)
* [Adafruit STEMMA QT cables](https://www.adafruit.com/product/4399) I used a 50mm QT-to-QT cable and a 100mm QT-to-bare wire cable.
## Other Parts
* 3D-printed case designed by ManelTo
* M2.5 heat-set inserts
* Soldering iron
* Aa box of M2.5 screws, sold as a laptop screw kit in various lengths.
## Process
1. Printed case files and inserted heat-set inserts, per ntindle's instructions.
2. Soldered QT cable to the keybow2040. Four wires: +3V, GND, SDA, SCL.
3. Mounted keybow2040, OLED, and encoder board in case with M2.5 screws. Assembled case.
4. Flashed CircuitPython UF2 (version 9.2 RC on mine)
5. Lots of trial and error.
6. Working code provided here.
