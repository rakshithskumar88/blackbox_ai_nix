{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.virtualenv
    python3Packages.pygobject3
    python3Packages.pycairo
    gtk3
    gobject-introspection
    gsettings-desktop-schemas
  ];

  # Set PYTHONPATH to find gobject-introspection
  PYTHONPATH = "${pkgs.python3Packages.pygobject3}/${pkgs.python3.sitePackages}";

  # Set GI_TYPELIB_PATH to find GObject-2.0.typelib
  GI_TYPELIB_PATH = "${pkgs.gobject-introspection}/lib/girepository-1.0";

  shellHook = ''
    # Add additional typelib paths
    export GI_TYPELIB_PATH="${pkgs.gtk3}/lib/girepository-1.0:${pkgs.pango}/lib/girepository-1.0:${pkgs.glib}/lib/girepository-1.0:$GI_TYPELIB_PATH"
    
    # Add library paths
    export LD_LIBRARY_PATH="${pkgs.gtk3}/lib:${pkgs.pango}/lib:${pkgs.glib}/lib:${pkgs.gobject-introspection}/lib"
    
    # Add GSettings schemas
    export XDG_DATA_DIRS="${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}:${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}:$XDG_DATA_DIRS"

    echo "Testing GObject availability..."
    python -c "import gi; from gi.repository import GObject" || echo "Warning: GObject not properly configured"

    echo "Testing GTK availability..."
    python -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" || echo "Warning: GTK not properly configured"

    # Create and activate virtual environment if it doesn't exist
    if [ ! -d .venv ]; then
      python -m venv .venv
      source .venv/bin/activate
      pip install -e .
    else
      source .venv/bin/activate
    fi

    echo "Development environment ready. You can run the application with: python -m blackbox_ai"
  '';
}
