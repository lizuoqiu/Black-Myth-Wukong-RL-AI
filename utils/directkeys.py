import ctypes
import time

# Setup for low-level keyboard input with ctypes
SendInput = ctypes.windll.user32.SendInput

# Hex key codes for your game
KEY_CODES = {
    'W': 0x11, 'A': 0x1E, 'S': 0x1F, 'D': 0x20,
    'M': 0x32, 'J': 0x24, 'K': 0x25, 'LSHIFT': 0x2A, 'R': 0x13,
    'V': 0x2F, 'Q': 0x10, 'I': 0x17, 'O': 0x18, 'P': 0x19,
    'C': 0x2E, 'F': 0x21, 'UP': 0xC8, 'DOWN': 0xD0,
    'LEFT': 0xCB, 'RIGHT': 0xCD, 'ESC': 0x01
}

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Function to press a key
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Function to release a key
def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Generalized function to press and release a key
def press_and_release(key, duration=0.1):
    PressKey(KEY_CODES[key])
    time.sleep(duration)
    ReleaseKey(KEY_CODES[key])

# Actions
def light_attack():
    press_and_release('J', 0.1)
    time.sleep(0.6)

def hard_attack():
    time.sleep(0.3)
    press_and_release('M', 0.1)
    time.sleep(2.0)

def hard_attack_long():
    PressKey(KEY_CODES['W'])
    PressKey(KEY_CODES['O'])
    PressKey(KEY_CODES['M'])
    time.sleep(4.5)
    ReleaseKey(KEY_CODES['M'])
    ReleaseKey(KEY_CODES['W'])
    ReleaseKey(KEY_CODES['O'])
    time.sleep(2.8)

def dodge():
    press_and_release('K', 0.1)
    time.sleep(0.35)

def combo_attack():
    for _ in range(4):
        light_attack()
    time.sleep(0.5)
    light_attack()
    time.sleep(0.5)

def left_dodge():
    PressKey(KEY_CODES['A'])
    dodge()
    ReleaseKey(KEY_CODES['A'])

def right_dodge():
    PressKey(KEY_CODES['D'])
    dodge()
    ReleaseKey(KEY_CODES['D'])

def power_attack():
    press_and_release('R', 0.1)
    combo_attack()

def block_break():
    light_attack()
    press_and_release('M', 0.1)
    time.sleep(2.0)