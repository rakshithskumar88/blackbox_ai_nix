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

3. Create a virtual environment with access to system packages:
```bash
# Create virtual environment with system packages access
python -m venv venv --system-site-packages
source venv/bin/activate

# Verify GTK packages are available
python -c "import gi" || echo "Error: GTK packages not found in PYTHONPATH"

# If the above command shows an error, try this NixOS-specific approach:
nix-shell -p python3Packages.pygobject3 python3Packages.pycairo --run "python -c 'import gi'"

# If that works, you can set up the environment permanently:
PYGI_PATH=$(nix-build --no-out-link '<nixpkgs>' -A python3Packages.pygobject3)
PYCAIRO_PATH=$(nix-build --no-out-link '<nixpkgs>' -A python3Packages.pycairo)
export PYTHONPATH="${PYGI_PATH}/lib/python3.10/site-packages:${PYCAIRO_PATH}/lib/python3.10/site-packages:${PYTHONPATH}"
```

4. Install the package:
```bash
# First upgrade pip to latest version
pip install --upgrade pip

# Install the package
pip install -e .
```

Note: If you still get "No module named 'gi'" error, try installing the package without a virtual environment:
```bash
pip install --user -e .
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
     * Make sure you created the virtual environment with `--system-site-packages`
     * Verify your NixOS configuration has the correct environment variables set (see Installation section)
     * Try using nix-shell for testing:
       ```bash
       nix-shell -p python3Packages.pygobject3 python3Packages.pycairo gtk3 gobject-introspection --run "python -c 'import gi; gi.require_version(\"Gtk\", \"3.0\"); from gi.repository import Gtk'"
       ```
   
   - If you get "Namespace Gtk not available" error:
     * Ensure GI_TYPELIB_PATH is set correctly in your NixOS configuration
     * Verify the environment variables are loaded:
       ```bash
       echo $GI_TYPELIB_PATH  # Should show paths containing girepository-1.0
       echo $LD_LIBRARY_PATH  # Should include GTK library paths
       ```
     * Try rebuilding your system: `sudo nixos-rebuild switch`
     * As a last resort, try running without a virtual environment: `pip install --user -e .`

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
