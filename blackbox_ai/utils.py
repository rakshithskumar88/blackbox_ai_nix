"""
Utility functions for logging and error handling.
"""

import logging
import sys
from functools import wraps
from typing import Callable, Any
from config import LOG_LEVEL, LOG_FORMAT

def setup_logging() -> None:
    """
    Configure the logging system for the application.
    """
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('blackbox_ai.log')
        ]
    )

def log_exceptions(func: Callable) -> Callable:
    """
    Decorator to log any exceptions that occur in the decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper

def safe_gtk_call(func: Callable) -> Callable:
    """
    Decorator to ensure GTK function calls are made from the main thread.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import GLib
        
        if not GLib.main_depth():
            GLib.idle_add(func, *args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper
