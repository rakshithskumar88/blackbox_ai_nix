{ pkgs ? import <nixpkgs> {} }:

let
  blackbox-ai = pkgs.callPackage ./default.nix {};
in
pkgs.mkShell {
  inputsFrom = [ blackbox-ai ];
  buildInputs = [ blackbox-ai ];

  shellHook = ''
    # Clean up any existing virtual environment
    if [ -d "venv" ]; then
      echo "Removing existing virtual environment..."
      rm -rf venv
    fi
    
    # Verify GTK is available
    echo "Testing GTK availability..."
    python -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" || echo "Warning: GTK not properly configured"

    echo "Development environment ready. You can run the application with: blackbox-ai"
  '';
}
