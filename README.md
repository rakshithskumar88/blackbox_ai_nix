# BlackboxAI for NixOS

A desktop AI assistant application for NixOS, inspired by the Mac Blackbox AI app. This application provides a floating window interface that can be toggled with a global hotkey, offering AI-powered assistance for developers.

## Features

- Global hotkey activation (Ctrl+Alt+B by default)
- Floating window interface that stays on top
- Modern, dark theme UI
- AI-powered chat interface
- Code explanation capabilities (future feature)
- System-wide accessibility

## Requirements

- NixOS
- Python 3.8 or higher
- GTK 3.0

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rakshithskumar88/blackbox_ai_nix.git
cd blackbox_ai_nix
```

2. Enter the development shell:
```bash
# This will set up a complete development environment with all dependencies
nix-shell

# The shell automatically:
# - Sets up Python with required packages (PyGObject, pycairo)
# - Sets up all GTK dependencies and environment variables
# - Verifies GTK availability
```

3. Install the package:
```bash
# Install in development mode
pip install -e .
```

After installation, you can run the application using either:
```bash
# Using the installed console script
blackbox-ai

# Or using the module directly
python -m blackbox_ai
```

## Usage

1. Use the global hotkey (Ctrl+Alt+B by default) to toggle the floating window.

2. Type your questions or code in the input field and press Enter or click Send.

## Configuration

You can modify the following settings in `blackbox_ai/config.py`:

- `HOTKEY`: Change the global hotkey combination
- `WINDOW_WIDTH` and `WINDOW_HEIGHT`: Adjust the window size
- `WINDOW_OPACITY`: Change the window transparency
- `LOG_LEVEL`: Modify logging verbosity

## Development

### Project Structure

```
blackbox_ai/
├── __init__.py          # Package initialization
├── main.py             # Application entry point
├── config.py           # Configuration settings
├── utils.py            # Utility functions
├── chat_service.py     # AI chat service implementation
├── hotkey_listener.py  # Global hotkey handling
└── ui/
    ├── main_window.py  # Main window implementation
    └── style.css       # GTK CSS styling
```

### Development Environment

The project includes a `shell.nix` file that sets up a complete development environment with all required dependencies. To use it:

1. Enter the development shell:
```bash
nix-shell
```

This will:
- Set up Python with GTK bindings (PyGObject) and Cairo
- Configure all required GTK environment variables
- Verify GTK availability

2. Start developing:
```bash
# Install in development mode
pip install -e .

# Run the application
blackbox-ai
```

### Running Tests

```bash
# TODO: Add testing instructions
```

## Troubleshooting

### Common Issues

1. **Global Hotkey Not Working**
   - Ensure you have the necessary permissions
   - Try running with sudo (not recommended for regular use)
   - Check if the hotkey is already in use by another application

2. **GTK Errors**
   - If you get GTK-related errors:
     * Make sure you're running the application from within the nix-shell
     * Try exiting the shell completely and entering it again: `exit` then `nix-shell`
     * Verify GTK is available in the shell:
       ```bash
       python -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk"
       ```

3. **Window Not Showing**
   - Check your window manager settings
   - Ensure no other application is blocking the window

### Logs

Logs are stored in `blackbox_ai.log` in the application directory. Check this file for detailed error information when troubleshooting.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the Mac Blackbox AI application
- Built with Python and GTK
- Thanks to the NixOS community

## Future Plans

- Integration with real AI services
- Code completion features
- File context awareness
- Customizable themes
- Plugin system
