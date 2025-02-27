"""
Configuration settings for the BlackboxAI application.
"""

import logging

# Hotkey Configuration
HOTKEY = "ctrl+alt+b"  # Default global hotkey to toggle the application

# Window Configuration
WINDOW_TITLE = "Blackbox AI"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_OPACITY = 0.95

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
    'background': '#1E1E1E',
    'text': '#FFFFFF',
    'input_background': '#2D2D2D',
    'input_text': '#FFFFFF',
    'user_message': '#007AFF',
    'ai_message': '#00FF00',
    'button_background': '#007AFF',
    'button_text': '#FFFFFF',
    'button_hover': '#0066CC',
    'toolbar_background': '#2D2D2D',
    'border': '#3C3C3C',
    'scrollbar': 'rgba(100, 100, 100, 0.7)',
    'scrollbar_hover': 'rgba(120, 120, 120, 0.8)'
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
