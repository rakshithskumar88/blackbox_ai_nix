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
- Python packages (see requirements.txt)

## Installation

1. First, ensure you have the required system dependencies. Add this to your NixOS configuration:

```nix
# configuration.nix
{ config, pkgs, ... }:

{
  # Required system packages
  environment.systemPackages = with pkgs; [
    python3
    python3Packages.pip
    gtk3
    gobject-introspection
    python3Packages.pygobject3
    python3Packages.pycairo
    ninja
    pkg-config
    cairo
    pango
    glib
  ];

  # Make GTK and Python packages available system-wide
  environment.variables = {
    # Add GTK libraries to library path
    LD_LIBRARY_PATH = lib.makeLibraryPath [
      pkgs.gtk3
      pkgs.gobject-introspection
    ];
    
    # Make Python packages available
    PYTHONPATH = lib.makeSearchPath "lib/python3.12/site-packages" [
      pkgs.python3Packages.pygobject3
      pkgs.python3Packages.pycairo
    ];
    
    # Ensure GI typelibs are found
    GI_TYPELIB_PATH = lib.makeSearchPath "lib/girepository-1.0" [
      pkgs.gtk3.out
      pkgs.pango.out
      pkgs.gobject-introspection
    ];
  };
}
```

After updating configuration.nix, rebuild your system:
```bash
sudo nixos-rebuild switch
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/blackbox-ai-nixos.git
cd blackbox-ai-nixos
```

3. Enter the development shell:
```bash
# This will create a virtual environment and set up all required dependencies
nix-shell

# The virtual environment will be automatically activated
# GTK availability will be verified automatically
```

4. Install the package:
```bash
# First upgrade pip to latest version
pip install --upgrade pip

# Install the package
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
- Create a Python virtual environment with system packages access
- Set up all required GTK environment variables
- Verify GTK availability
- Activate the virtual environment automatically

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
   - If you get "No module named 'gi'" error:
     * Make sure you're using the provided development shell: `nix-shell`
     * Verify your NixOS configuration has the correct environment variables set
     * Try rebuilding your system: `sudo nixos-rebuild switch`
   
   - If you get "Namespace Gtk not available" error:
     * Ensure you're using the development shell: `nix-shell`
     * Verify the environment variables are loaded:
       ```bash
       echo $GI_TYPELIB_PATH  # Should show paths containing girepository-1.0
       echo $LD_LIBRARY_PATH  # Should include GTK library paths
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
