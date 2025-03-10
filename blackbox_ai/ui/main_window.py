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
    WINDOW_OPACITY, STYLE_PATH, TOOLBAR_BUTTONS,
    INPUT_PLACEHOLDER, API_ENDPOINTS, WINDOW_SUBTITLE,
    SHORTCUTS
)
from ..utils import log_exceptions, safe_gtk_call

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=WINDOW_TITLE)
        
        # Set up window properties
        self.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_keep_above(True)  # Keep window on top
        self.set_opacity(WINDOW_OPACITY)
        
        # Set up header bar
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.set_title(WINDOW_TITLE)
        header_bar.set_subtitle(WINDOW_SUBTITLE)
        self.set_titlebar(header_bar)
        
        # Add VSCode button to header bar
        vscode_button = Gtk.Button()
        vscode_button.set_tooltip_text("Open in VSCode")
        vscode_icon = Gtk.Image.new_from_icon_name("applications-development", Gtk.IconSize.LARGE_TOOLBAR)
        vscode_button.add(vscode_icon)
        header_bar.pack_end(vscode_button)
        
        # Add menu button to header bar
        menu_button = Gtk.MenuButton()
        menu_button.set_tooltip_text("Menu")
        menu_icon = Gtk.Image.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        menu_button.add(menu_icon)
        
        # Create menu
        menu = Gtk.Menu()
        
        # Add menu items with shortcuts
        for shortcut_name, shortcut_key in SHORTCUTS.items():
            if shortcut_name != 'toggle_window':  # Skip global hotkey
                menu_item = Gtk.MenuItem.new_with_label(
                    f"{shortcut_name.replace('_', ' ').title()} ({shortcut_key})"
                )
                menu.append(menu_item)
        
        menu.show_all()
        menu_button.set_popup(menu)
        header_bar.pack_end(menu_button)
        
        # Load CSS styling
        self._load_css()
        
        # Set up keyboard shortcuts
        self._setup_shortcuts()
        
        # Set up the UI layout
        self._setup_ui()
        
        # Connect window signals
        self.connect("delete-event", self.on_delete_event)
        
    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)
        
        # Clear chat shortcut
        key, mod = Gtk.accelerator_parse(SHORTCUTS['clear_chat'])
        accel_group.connect(key, mod, Gtk.AccelFlags.VISIBLE, 
                          lambda *x: self.chat_buffer.set_text(""))
        
        # New chat shortcut
        key, mod = Gtk.accelerator_parse(SHORTCUTS['new_chat'])
        accel_group.connect(key, mod, Gtk.AccelFlags.VISIBLE,
                          lambda *x: self._new_chat())
        
        # Close window shortcut
        key, mod = Gtk.accelerator_parse(SHORTCUTS['close_window'])
        accel_group.connect(key, mod, Gtk.AccelFlags.VISIBLE,
                          lambda *x: self.hide())
        
    def _new_chat(self):
        """Start a new chat session."""
        self.chat_buffer.set_text("")
        self.message_entry.set_text("")
        
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

    def _create_button_with_icon(self, label, icon_name, tooltip=None, shortcut=None):
        """Create a button with both icon and label."""
        button = Gtk.Button()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Create icon
        icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.SMALL_TOOLBAR)
        box.pack_start(icon, False, False, 0)
        
        # Create label with shortcut
        label_text = f"{label} ({shortcut})" if shortcut else label
        label_widget = Gtk.Label(label=label_text)
        box.pack_start(label_widget, True, True, 0)
        
        button.add(box)
        
        # Add tooltip if provided
        if tooltip:
            button.set_tooltip_text(tooltip)
            
        return button

    @log_exceptions
    def _setup_ui(self):
        """Set up the user interface components."""
        # Create main vertical box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # Create toolbar
        toolbar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar_box.get_style_context().add_class("toolbar")
        main_box.pack_start(toolbar_box, False, False, 0)

        # Add model selection combobox
        model_store = Gtk.ListStore(str)
        models = list(API_ENDPOINTS.keys())
        for model in models:
            model_store.append([model])
        
        model_combo = Gtk.ComboBox.new_with_model(model_store)
        renderer_text = Gtk.CellRendererText()
        model_combo.pack_start(renderer_text, True)
        model_combo.add_attribute(renderer_text, "text", 0)
        model_combo.set_active(0)
        model_combo.set_tooltip_text("Select AI model")
        toolbar_box.pack_start(model_combo, False, False, 6)

        # Add toolbar buttons with icons, tooltips, and shortcuts
        for button_config in TOOLBAR_BUTTONS:
            button = self._create_button_with_icon(
                button_config['label'],
                button_config['icon'],
                button_config['tooltip'],
                button_config['shortcut']
            )
            toolbar_box.pack_start(button, False, False, 2)

        # Create chat display area
        self.chat_display = Gtk.TextView()
        self.chat_display.set_wrap_mode(Gtk.WrapMode.WORD)
        self.chat_display.set_editable(False)
        self.chat_buffer = self.chat_display.get_buffer()

        # Create text tags
        self.chat_buffer.create_tag("user-message", foreground="#007aff")
        self.chat_buffer.create_tag("ai-message", foreground="#000000")

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
        self.message_entry.set_placeholder_text(INPUT_PLACEHOLDER)
        self.message_entry.connect("activate", self.on_send_clicked)
        input_box.pack_start(self.message_entry, True, True, 10)
        
        # Create send button with icon
        send_button = self._create_button_with_icon(
            "Send",
            "mail-send",
            "Send message (Enter)"
        )
        send_button.connect("clicked", self.on_send_clicked)
        input_box.pack_start(send_button, False, False, 10)
        
        main_box.pack_start(input_box, False, False, 10)

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
