"""
Configuration settings for the BlackboxAI application.
"""

import logging

# Hotkey Configuration
HOTKEY = "ctrl+alt+b"  # Default global hotkey to toggle the application

# Window Configuration
WINDOW_TITLE = "Ask Blackbox AI Anything"
WINDOW_WIDTH = 1024  # Match Mac app width
WINDOW_HEIGHT = 768  # Match Mac app height
WINDOW_OPACITY = 1.0  # Full opacity like Mac app
WINDOW_SUBTITLE = "Join +10M users & Fortune 500 companies using the Most Advanced Coding Agent on VSCode #1 on SWE Bench"

# UI Configuration
STYLE_PATH = "style.css"
FONT_FAMILY = "Ubuntu"
FONT_SIZE = "14px"

# Model Configuration
DEFAULT_MODEL = "DeepSeek-V3"
MODEL_TIMEOUT = 30  # seconds

# API Configuration
API_ENDPOINTS = {
    "DeepSeek-V3": "https://api.deepseek.com/v3/chat",
    "DeepSeek-R1": "https://api.deepseek.com/r1/chat",
    "Meta-Llama-3.3-70B": "https://api.meta.com/llama/v3.3/chat",
    "Gemini-Flash-2.0": "https://api.google.com/gemini/flash/v2/chat",
    "GPT-4o": "https://api.openai.com/v1/chat",
    "Claude-Sonnet-3.7": "https://api.anthropic.com/v1/chat"
}

API_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Chat Configuration
MAX_CONTEXT_LENGTH = 4096
MAX_MESSAGE_LENGTH = 2000
MAX_HISTORY_MESSAGES = 100
TYPING_SIMULATION_SPEED = 50  # characters per second

# Web Search Configuration
SEARCH_RESULT_LIMIT = 5
SEARCH_TIMEOUT = 10  # seconds

# Logging Configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'blackbox_ai.log'

# Theme Configuration
THEME = {
    'background': '#ffffff',
    'text': '#000000',
    'input_background': '#f5f5f5',
    'input_text': '#000000',
    'user_message': '#007aff',
    'ai_message': '#000000',
    'button_background': '#007aff',
    'button_text': '#ffffff',
    'button_hover': '#0066cc',
    'toolbar_background': '#f5f5f5',
    'border': '#e0e0e0',
    'scrollbar': 'rgba(0, 0, 0, 0.2)',
    'scrollbar_hover': 'rgba(0, 0, 0, 0.3)',
    'header_background': 'linear-gradient(to bottom, #ffffff, #f5f5f5)',
    'header_text': '#000000',
    'header_subtitle': '#666666'
}

# Feature Flags
FEATURES = {
    'web_search': True,
    'deep_research': True,
    'code_explanation': True,
    'multi_model': True,
    'file_upload': True,
    'image_generation': True,
    'beast_mode': True,
    'customize': True
}

# Development Settings
DEBUG = False
SIMULATE_API = True  # Use simulated responses for development

# Toolbar Configuration
TOOLBAR_BUTTONS = [
    {
        'label': 'Web Search',
        'icon': 'system-search',
        'tooltip': 'Search the web for information',
        'shortcut': 'Ctrl+F'
    },
    {
        'label': 'Deep Research',
        'icon': 'edit-find',
        'tooltip': 'Perform in-depth research',
        'shortcut': 'Ctrl+R'
    },
    {
        'label': 'Models',
        'icon': 'applications-science',
        'tooltip': 'Select AI model',
        'shortcut': 'Ctrl+M'
    },
    {
        'label': 'Beast Mode',
        'icon': 'weather-storm',
        'tooltip': 'Enable advanced features',
        'shortcut': 'Ctrl+B'
    },
    {
        'label': 'Image',
        'icon': 'image-x-generic',
        'tooltip': 'Generate or analyze images',
        'shortcut': 'Ctrl+I'
    },
    {
        'label': 'Upload',
        'icon': 'document-send',
        'tooltip': 'Upload files for analysis',
        'shortcut': 'Ctrl+U'
    },
    {
        'label': 'Customize',
        'icon': 'preferences-system',
        'tooltip': 'Customize settings',
        'shortcut': 'Ctrl+,'
    },
    {
        'label': 'Multi-Panel',
        'icon': 'view-grid',
        'tooltip': 'Open multiple chat panels',
        'shortcut': 'Ctrl+T'
    }
]

# Input Configuration
INPUT_PLACEHOLDER = "Message Blackbox or @mention agent"

# Window Shadow
WINDOW_SHADOW = {
    'enabled': True,
    'radius': 20,
    'opacity': 0.15,
    'offset_x': 0,
    'offset_y': 2
}

# Animation Settings
ANIMATIONS = {
    'enabled': True,
    'duration': 200,  # milliseconds
    'easing': 'ease-out'
}

# Keyboard Shortcuts
SHORTCUTS = {
    'toggle_window': 'Ctrl+Alt+B',
    'send_message': 'Enter',
    'clear_chat': 'Ctrl+L',
    'new_chat': 'Ctrl+N',
    'close_window': 'Escape'
}
