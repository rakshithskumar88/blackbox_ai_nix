"""
Hotkey listener implementation for the BlackboxAI application.
"""

import logging
import threading
from typing import Callable
import evdev
from evdev import ecodes, InputEvent
from select import select

from .config import HOTKEY
from .utils import log_exceptions

logger = logging.getLogger(__name__)

class HotkeyListener:
    """
    Listens for global hotkeys and triggers callbacks when detected.
    """
    def __init__(self, callback: Callable[[], None]):
        """
        Initialize the hotkey listener.
        
        Args:
            callback: Function to call when hotkey is detected
        """
        self._callback = callback
        self._running = False
        self._thread = None
        self._keys_pressed = set()
        self._hotkey_parts = HOTKEY.lower().split('+')
        self._key_mapping = {
            'ctrl': ecodes.KEY_LEFTCTRL,
            'alt': ecodes.KEY_LEFTALT,
            'b': ecodes.KEY_B
        }
        self._devices = []

    def start(self):
        """Start listening for hotkeys."""
        if self._thread is not None:
            return

        try:
            # Find all keyboard devices
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            self._devices = [dev for dev in devices if self._is_keyboard(dev)]
            
            if not self._devices:
                logger.error("No keyboard devices found")
                return

            self._running = True
            self._thread = threading.Thread(target=self._run_listener)
            self._thread.daemon = True
            self._thread.start()
            logger.info(f"Started hotkey listener for {HOTKEY}")

        except Exception as e:
            logger.error(f"Error in hotkey listener: {str(e)}")
            self._running = False

    def stop(self):
        """Stop listening for hotkeys."""
        self._running = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    @log_exceptions
    def _run_listener(self):
        """Main listener loop."""
        try:
            while self._running:
                r, w, x = select(self._devices, [], [], 0.1)
                for dev in r:
                    try:
                        for event in dev.read():
                            if event.type == ecodes.EV_KEY:
                                self._handle_key_event(event)
                    except Exception as e:
                        logger.error(f"Error reading device events: {str(e)}")
                        continue

        except Exception as e:
            logger.error(f"Error in listener loop: {str(e)}")
        finally:
            for dev in self._devices:
                dev.close()

    def _handle_key_event(self, event: InputEvent):
        """Handle a single key event."""
        if event.type != ecodes.EV_KEY:
            return

        key_code = event.code
        if event.value == 1:  # Key pressed
            self._keys_pressed.add(key_code)
        elif event.value == 0:  # Key released
            self._keys_pressed.discard(key_code)

        # Check if hotkey combination is pressed
        required_keys = set(self._key_mapping[part] for part in self._hotkey_parts)
        if required_keys.issubset(self._keys_pressed):
            self._callback()

    def _is_keyboard(self, device: evdev.InputDevice) -> bool:
        """Check if a device is a keyboard."""
        return (
            ecodes.EV_KEY in device.capabilities() and
            ecodes.KEY_A in device.capabilities().get(ecodes.EV_KEY, [])
        )
