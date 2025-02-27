"""
Main window implementation for the BlackboxAI application.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import logging
from pathlib import Path

from ..config import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    WINDOW_OPACITY, STYLE_PATH
)
from ..utils import log_exceptions, safe_gtk_call

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=WINDOW_TITLE)
        
        # Set up window properties
        self.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_keep_above(True)  # Keep window on top
        self.set_opacity(WINDOW_OPACITY)
        
        # Load CSS styling
        self._load_css()
        
        # Set up the UI layout
        self._setup_ui()
        
        # Connect window signals
        self.connect("delete-event", self.on_delete_event)
        
    @log_exceptions
    def _load_css(self):
        """Load and apply CSS styling."""
        css_provider = Gtk.CssProvider()
        css_file = Path(__file__).parent / STYLE_PATH
        css_provider.load_from_path(str(css_file))
        
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    @log_exceptions
    def _setup_ui(self):
        """Set up the user interface components."""
        # Create main vertical box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(main_box)

        # Create chat display area
        self.chat_display = Gtk.TextView()
        self.chat_display.set_wrap_mode(Gtk.WrapMode.WORD)
        self.chat_display.set_editable(False)
        self.chat_buffer = self.chat_display.get_buffer()

        # Create text tags
        self.chat_buffer.create_tag("user-message", foreground="blue")
        self.chat_buffer.create_tag("ai-message", foreground="green")

        # Add chat display to a scrolled window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC
        )
        scrolled_window.add(self.chat_display)
        main_box.pack_start(scrolled_window, True, True, 0)

        # Create input area
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Create message entry
        self.message_entry = Gtk.Entry()
        self.message_entry.set_placeholder_text("Type your message here...")
        self.message_entry.connect("activate", self.on_send_clicked)
        input_box.pack_start(self.message_entry, True, True, 0)
        
        # Create send button
        send_button = Gtk.Button.new_with_label("Send")
        send_button.connect("clicked", self.on_send_clicked)
        input_box.pack_start(send_button, False, False, 0)
        
        main_box.pack_start(input_box, False, False, 0)

    @safe_gtk_call
    def append_message(self, message: str, is_user: bool = True):
        """
        Append a message to the chat display.
        
        Args:
            message: The message to append
            is_user: True if the message is from the user, False if from AI
        """
        end_iter = self.chat_buffer.get_end_iter()
        
        # Add newline if buffer is not empty
        if self.chat_buffer.get_char_count() > 0:
            self.chat_buffer.insert(end_iter, "\n")
        
        # Insert the message with appropriate tags
        tag_name = "user-message" if is_user else "ai-message"
        prefix = "You: " if is_user else "AI: "
        
        self.chat_buffer.insert_with_tags_by_name(
            end_iter,
            f"{prefix}{message}",
            tag_name
        )
        
        # Scroll to the bottom
        adj = self.chat_display.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    @log_exceptions
    def on_send_clicked(self, widget):
        """Handle send button clicks and Enter key in message entry."""
        message = self.message_entry.get_text().strip()
        if message:
            self.append_message(message, is_user=True)
            self.message_entry.set_text("")
            # Signal that we have a new message
            GLib.idle_add(self._process_message, message)

    def _process_message(self, message: str):
        """Process the user's message and get AI response."""
        # TODO: Implement actual AI service integration
        # For now, just echo the message back
        response = f"Echo: {message}"
        self.append_message(response, is_user=False)
        return False

    def toggle_visibility(self):
        """Toggle the window's visibility."""
        if self.get_visible():
            self.hide()
        else:
            self.show_all()

    def on_delete_event(self, widget, event):
        """Handle window close event."""
        self.hide()
        return True  # Prevent the window from being destroyed
