"""
Main entry point for the BlackboxAI application.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import logging
import signal
import sys

from .ui.main_window import MainWindow
from .hotkey_listener import HotkeyListener
from .chat_service import ChatService
from .utils import setup_logging, log_exceptions

logger = logging.getLogger(__name__)

class BlackboxAI:
    def __init__(self):
        """Initialize the BlackboxAI application."""
        # Set up logging
        setup_logging()
        logger.info("Starting BlackboxAI application")

        # Initialize components
        self.window = None
        self.hotkey_listener = None
        self.chat_service = None

    @log_exceptions
    def initialize(self):
        """Initialize all components of the application."""
        try:
            # Initialize the main window
            self.window = MainWindow()
            
            # Initialize the chat service
            self.chat_service = ChatService()
            
            # Initialize and start the hotkey listener
            self.hotkey_listener = HotkeyListener(self.toggle_window)
            self.hotkey_listener.start()

            # Set up signal handlers for graceful shutdown
            GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, self.quit)
            GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTERM, self.quit)

            logger.info("BlackboxAI initialization complete")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize BlackboxAI: {str(e)}")
            return False

    @log_exceptions
    def toggle_window(self):
        """Toggle the main window visibility."""
        if self.window:
            GLib.idle_add(self.window.toggle_visibility)

    @log_exceptions
    def run(self):
        """Run the application."""
        try:
            if not self.initialize():
                logger.error("Failed to initialize. Exiting.")
                return 1

            # Show the main window
            self.window.show_all()
            
            # Start the GTK main loop
            Gtk.main()
            return 0

        except Exception as e:
            logger.error(f"Error running BlackboxAI: {str(e)}")
            return 1

        finally:
            self.cleanup()

    @log_exceptions
    def quit(self):
        """Quit the application."""
        logger.info("Shutting down BlackboxAI")
        Gtk.main_quit()
        return False

    @log_exceptions
    def cleanup(self):
        """Clean up resources before exit."""
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        
        if self.chat_service:
            self.chat_service.close()
        
        logger.info("Cleanup complete")

def main():
    """Main entry point."""
    app = BlackboxAI()
    sys.exit(app.run())

if __name__ == "__main__":
    main()
