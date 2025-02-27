"""
Global hotkey listener implementation for the BlackboxAI application.
"""

import logging
import threading
from typing import Callable
import keyboard
from .config import HOTKEY
from .utils import log_exceptions

logger = logging.getLogger(__name__)

class HotkeyListener:
    def __init__(self, callback: Callable[[], None]):
        """
        Initialize the hotkey listener.
        
        Args:
            callback: Function to call when the hotkey is pressed
        """
        self.callback = callback
        self.running = False
        self.thread = None
        self.logger = logging.getLogger(__name__)

    @log_exceptions
    def start(self):
        """Start listening for the global hotkey."""
        if self.running:
            self.logger.warning("Hotkey listener is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_listener)
        self.thread.daemon = True  # Thread will exit when main program exits
        self.thread.start()
        self.logger.info(f"Started hotkey listener for {HOTKEY}")

    @log_exceptions
    def stop(self):
        """Stop listening for the global hotkey."""
        if not self.running:
            return

        self.running = False
        if self.thread:
            keyboard.unhook_all()  # Remove all keyboard hooks
            self.thread.join()
            self.thread = None
        self.logger.info("Stopped hotkey listener")

    @log_exceptions
    def _run_listener(self):
        """Run the hotkey listener in a separate thread."""
        try:
            keyboard.add_hotkey(HOTKEY, self._handle_hotkey)
            self.logger.info(f"Registered hotkey: {HOTKEY}")
            
            # Keep the thread alive
            while self.running:
                keyboard.wait()
        except Exception as e:
            self.logger.error(f"Error in hotkey listener: {str(e)}")
            self.running = False
        finally:
            keyboard.unhook_all()

    @log_exceptions
    def _handle_hotkey(self):
        """Handle the hotkey press event."""
        if self.running and self.callback:
            try:
                self.callback()
                self.logger.debug("Hotkey callback executed successfully")
            except Exception as e:
                self.logger.error(f"Error in hotkey callback: {str(e)}")

    def is_running(self) -> bool:
        """Check if the listener is currently running."""
        return self.running
