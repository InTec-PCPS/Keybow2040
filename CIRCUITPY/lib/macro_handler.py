# SPDX-FileCopyrightText: 2022 Nox Ferocia
#
# SPDX-License-Identifier: Unlicense

'''
Unified Macro Handler (/lib/macro_handler.py)
Written in Adafruit Circuit Python for
SOFTWARE: adafruit_hid Library
==========
Provides a composite of the default adafruit_hid interfacces,
macro handlers to simplfiy coding / macro writing, and an
extensible framework for additional custom macro handlers
'''

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.Mouse import Mouse

class HIDPool( object ):
	'''
	Composite Pool of all default adafruit_hid interfaces
	Aliases:
		.key: adafruit_hid.keyboard.Keyboard
		.media: adafruit_hid.consumer_control.ConsumerControl
		.mouse: adafruit_hid.mouse.Mouse
		.text: adafruit_hid.keyboard_layout_us.KeyboardLayoutUS
	'''
	key = Keyboard( usb_hid.devices )
	media = ConsumerControl( usb_hid.devices )
	mouse = Mouse( usb_hid.devices )
	text = KeyboardLayoutUS( key )
	
# Workaround for bad assumption in adafruit_hid.keyboard.Keyboard.send
def parse_mod_plus( *macro_data ) -> None:
	'''
	Presses modifier keys, sends regular
	keys individually, releases modifer keys
	macro_data Format:
		modifer, ..., flag, regular, ...
	Parameters:
		modifer: integer, key code, 1-5 modifiers, eg ALT
		flag: string, "MOD_PLUS", exactly
		regular: integer, key code, 1+ additional keys, eg F4
	'''
	_held_flag = True
	for _key_code in macro_data:
		if "MOD+" == _key_code:
			_held_flag = False
			continue
		if _held_flag:
			HIDPool.key.press( _key_code )
		else:
			HIDPool.key.press( _key_code )
			HIDPool.key.release( _key_code )
	for _key_code in reversed( macro_data ):
		if "MOD+" == _key_code:
			_held_flag = True
			continue
		if _held_flag:
			HIDPool.key.release( _key_code )

# Workaround for bad assumption in adafruit_hid.keyboard_layout_us.KeyboardLayoutUS.write
def parse_utf16( target_platform, utf16_code ) -> None:
	'''
	Sends keystrokes to enter a UTF16 character on the target platform
	"NIX": ChromeOS / Linux, "WIN":windows xp+, "MAC": MAcOS 8.5+
	Windows and MacOS both require enabling Unicode Hex entry for this to work
	Parameters:
		target_platform: string, "NIX", "WIN", "MAC"
		utf16_code: string, 4 hexadecimal digits
	See Also:
		https://en.wikipedia.org/wiki/Unicode_input#Hexadecimal_input
	'''
	if "NIX" == target_platform:
		HIDPool.key.press( 0xE4, 0xE5, 0x18 )
		HIDPool.key.release( 0x18 )
	elif "WIN" == target_platform:
		HIDPool.key.press( 0xE6 )
		HIDPool.key.press( 0x57 )
		HIDPool.key.release( 0x57 )
	elif "MAC" == target_platform:
		HIDPool.key.press( 0xE2 )
	for _hex_digit in utf16_code:
		# Use last index returned for safety with capitlized hex
		_hex_keycode = HIDPool.text.keycodes( _hex_digit )[-1]
		HIDPool.key.press( _hex_keycode )
		HIDPool.key.release( _hex_keycode )
	if "MAC" == target_platform:
		HIDPool.key.release( 0xE2 )
	elif "WIN" == target_platform:
		HIDPool.key.release( 0xE6 )
	elif "NIX" == target_platform:
		HIDPool.key.release( 0xE5, 0xE4 )

def parse_mouse_select( mouse_buttons, x_axis, y_axis, scroll ) -> None:
	'''
	Presses specified mouse buttons, moves/scrolls mouse, releases mouse buttons
	Parameters:
		mouse_buttons: integer, sum of desired buttons, (1:left, 2:right, 4:middle)
		x_axis: integer, +right/-left, 0-127, horizontal axis movement
		y_axis: integer, +up/-down, 0-127, vertical axis movement
		scroll: integer, +up/-down, 0-127, scroll wheel movement
	'''
	HIDPool.mouse.press( mouse_buttons )
	HIDPool.mouse.move( x_axis, y_axis, scroll )
	HIDPool.mouse.release( mouse_buttons )

_macro_parsers = {
"MOD+": parse_mod_plus,
"UTF16": parse_utf16,
"MOUSE SELECT": parse_mouse_select,
}

class MacroHandler( HIDPool ):
	'''
	Composite aggregator class for sending HID macros
	'''
	MACRO_TYPE = 0
	MACRO_DATA = 1
	# TODO: potentially move attributes here
	
	def __init__( self, parser_dictionary = _macro_parsers ) -> None:
		'''
		Adds dictionary of parser functions to the instance
		Creates aliases to aggregate HID communications
		Parameter:
			parser_dictionary: dictionary, {"parser id": parser_function, ...}
		'''
		self.__internal_parsers = {
		"KEY": self.key.send,
		"MEDIA": self.media.send,
		"MOUSE CLICK": self.mouse.click,
		"MOUSE MOVE": self.mouse.move,
		"TEXT": self.text.write,
		}
		
		self.__external_parsers = parser_dictionary
	
	def send_macro( self, macro_container ) -> None:
		'''
		Checks type of macro container and processes accordingly.
		macro_container Format: (either of)
			tuple: ("PARSER_ID", PARSER_MACRO)
			List: [("PARSER_ID", PARSER_MACRO), ...]
		Parameter:
			macro: tuple, ( "PARSER_ID", PARSER_MACRO )
				"PARSER_ID": string, id of a parser
				PARSER_MACRO: varies, see related function
		For builtin parser IDs SEE ALSO:
			KEY: adafruit_hid.keyboard.Keyboard.send
			MEDIA: adafruit_hid.consumer_control.ConsumerControl.send
			MOUSE_CLICK: adafruit_hid.mouse.Mouse.send
			MOUSE_MOVE: adafruit_hid.mouse.Mouse.move
			TEXT: adafruit_hid.keyboard_layout_us.KeyboardLayoutUS.write
		'''
		if tuple == type( macro_container ):
			macro_container = [macro_container]
		for _macro in macro_container:
			if _macro[ self.MACRO_TYPE ] in self.__internal_parsers:
				self.__internal_parsers[ _macro[ self.MACRO_TYPE ] ]( *_macro[ self.MACRO_DATA: ] )
			elif _macro[ self.MACRO_TYPE ] in self.__external_parsers:
				self.__external_parsers[ _macro[ self.MACRO_TYPE ] ]( *_macro[ self.MACRO_DATA: ] )
	
	def get_handler_list( self ) -> list:
		'''
		Returns:
			Dictionary, {Parser id, function} pairs
		'''
		return sorted( self.__internal_parsers ) + sorted( self.__external_parsers.copy() )
	
	def add_handler( self, new_id, new_function, override = False ) -> bool:
		'''
		Adds a new external parser to the dictionary
		Parameters:
			new_id: string, id for parser function
			new_function: function name, without ()
			override: boolean, optional, True to replace preexisting id
				"KEY", "MEDIA", "MOUSE_CLICK", "MOUSE_MOVE", & "TEXT" cannot be added/overridden
		Returns:
			boolean, True if successful, False if denied
		'''
		if new_id in self.__internal_parsers or (new_id in self.__external_parsers and not override):
			return False
		self.__external_parsers[new_id] = new_function
		return True
	
	def del_handler( self, remove_id ) -> bool:
		'''
		Removes an external parser from the dictionary
		Parameter:
			remove_id: string, id of a parser in the dictionary
		Returns:
			boolean, True if removed, False otherwise
				"KEY", "MEDIA", "MOUSE_CLICK", "MOUSE_MOVE", & "TEXT" cannot be removed
		'''
		if remove_id not in self.__external_parsers:
			return False
		self.__external_parsers.pop( remove_id )
		return True