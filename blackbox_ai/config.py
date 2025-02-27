"""
Configuration settings for the BlackboxAI application.
"""

import logging

# Hotkey Configuration
HOTKEY = "ctrl+alt+b"  # Default global hotkey to toggle the application

# Window Configuration
WINDOW_TITLE = "Blackbox AI"
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
WINDOW_OPACITY = 0.95

# UI Configuration
STYLE_PATH = "style.css"
FONT_FAMILY = "Ubuntu"
FONT_SIZE = "12px"

# Logging Configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Chat Configuration
MAX_MESSAGE_HISTORY = 100
SIMULATED_RESPONSE_DELAY = 1.0  # seconds

# API Configuration (for future use with real AI service)
API_ENDPOINT = "https://api.example.com/v1/chat"
API_TIMEOUT = 10  # seconds
