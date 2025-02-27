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

### Development Installation

1. Clone the repository:
```bash
git clone https://github.com/rakshithskumar88/blackbox_ai_nix.git
cd blackbox_ai_nix
```

2. Enter the development shell:
```bash
# This will set up a complete development environment with all dependencies
nix-shell
```

3. Run the application:
```bash
blackbox-ai
```

### System Installation

To install the application system-wide:

```bash
# Build and install using Nix
nix-env -f default.nix -i
```

Or add it to your NixOS configuration:

```nix
# configuration.nix
{
  environment.systemPackages = [
    (pkgs.callPackage /path/to/blackbox_ai_nix/default.nix {})
  ];
}
```

Then rebuild your system:
```bash
sudo nixos-rebuild switch
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

The project uses Nix for reproducible builds and development environments:

- `default.nix`: Defines the application build
- `shell.nix`: Provides a development environment

The development shell automatically:
- Sets up Python with GTK bindings
- Configures all required GTK environment variables
- Makes the application available in PATH

### Building

To build the application:
```bash
nix-build
```

This will create a `result` symlink pointing to the built package.

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
   - Make sure you're running the application from within the nix-shell
   - Try rebuilding the development environment:
     ```bash
     # Exit current shell if any
     exit
     
     # Remove result if it exists
     rm -f result
     
     # Enter shell again
     nix-shell
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
