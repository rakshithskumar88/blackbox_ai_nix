{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.virtualenv
    python3Packages.pygobject3
    python3Packages.pycairo
    gtk3
    gobject-introspection
    pkg-config
    cairo
    pango
    glib
    ninja
  ];

  shellHook = ''
    # Set up environment variables
    export GI_TYPELIB_PATH="${pkgs.gtk3}/lib/girepository-1.0:${pkgs.pango}/lib/girepository-1.0:${pkgs.glib}/lib/girepository-1.0:${pkgs.gobject-introspection}/lib/girepository-1.0"
    export LD_LIBRARY_PATH="${pkgs.gtk3}/lib:${pkgs.pango}/lib:${pkgs.glib}/lib:${pkgs.cairo}/lib"
    export XDG_DATA_DIRS="${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}:${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}:$XDG_DATA_DIRS"
    
    # Create venv if it doesn't exist
    if [ ! -d "venv" ]; then
      python -m venv venv --system-site-packages
    fi
    
    # Activate venv
    source venv/bin/activate
    
    # Verify GTK is available
    python -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" || echo "Warning: GTK not properly configured"
  '';
}
