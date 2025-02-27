"""
Main entry point for the BlackboxAI application.
"""

import asyncio
import logging
import signal
import sys
from gi.repository import GLib

from .ui.main_window import MainWindow
from .hotkey_listener import HotkeyListener
from .chat_service import ChatService
from .utils import setup_logging

logger = logging.getLogger(__name__)

class BlackboxAI:
    """
    Main application class for BlackboxAI.
    """
    def __init__(self):
        self.window = None
        self.hotkey_listener = None
        self.chat_service = None
        self.loop = None

    async def initialize(self):
        """Initialize the application."""
        try:
            # Set up logging
            setup_logging()
            logger.info("Starting BlackboxAI application")

            # Initialize chat service
            self.chat_service = ChatService()
            await self.chat_service.initialize()

            # Create main window
            self.window = MainWindow()
            self.window.connect("destroy", self.cleanup)

            # Set up message processing
            def process_message_callback(message):
                asyncio.create_task(self._process_message(message))

            self.window._process_message = process_message_callback

            # Initialize hotkey listener
            self.hotkey_listener = HotkeyListener(self.window.toggle_visibility)
            self.hotkey_listener.start()

            logger.info("BlackboxAI initialization complete")

        except Exception as e:
            logger.error(f"Failed to initialize BlackboxAI: {str(e)}")
            await self.cleanup()
            sys.exit(1)

    async def _process_message(self, message: str):
        """Process a message through the chat service."""
        try:
            response = await self.chat_service.process_message(message)
            
            # Schedule UI update in main thread
            GLib.idle_add(
                self.window.append_message,
                response,
                False  # is_user=False for AI responses
            )

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            GLib.idle_add(
                self.window.append_message,
                f"Error: {str(e)}",
                False
            )

    async def cleanup(self, *args):
        """Clean up resources."""
        logger.info("Cleaning up...")
        
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        
        if self.chat_service:
            await self.chat_service.cleanup()
        
        logger.info("Cleanup complete")

def main():
    """Main entry point."""
    app = BlackboxAI()
    loop = asyncio.get_event_loop()

    try:
        # Initialize the application
        loop.run_until_complete(app.initialize())

        # Set up signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(app.cleanup()))

        # Show the window
        app.window.show_all()

        # Start the GTK main loop
        GLib.MainLoop().run()

    except Exception as e:
        logger.error(f"Failed to initialize. Exiting.")
        loop.run_until_complete(app.cleanup())
        sys.exit(1)

if __name__ == "__main__":
    main()
