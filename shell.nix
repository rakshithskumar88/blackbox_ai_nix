{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    pip
    pygobject3
    pycairo
  ]);
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    pythonEnv
    gtk3
    gtk3.dev
    gobject-introspection
    pkg-config
    cairo
    cairo.dev
    pango
    pango.dev
    glib
    glib.dev
    gsettings-desktop-schemas
    ninja
    wrapGAppsHook
  ];

  nativeBuildInputs = with pkgs; [
    wrapGAppsHook
  ];

  # Enable GDK pixbuf loaders
  GDK_PIXBUF_MODULE_FILE = "${pkgs.librsvg}/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache";

  shellHook = ''
    # Set up environment variables
    export XDG_DATA_DIRS="${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}:${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}:$XDG_DATA_DIRS"
    
    # Set GI paths
    export GI_TYPELIB_PATH="${pkgs.gtk3}/lib/girepository-1.0:${pkgs.pango}/lib/girepository-1.0:${pkgs.glib}/lib/girepository-1.0:${pkgs.gobject-introspection}/lib/girepository-1.0"
    
    # Set library paths
    export LD_LIBRARY_PATH="${pkgs.gtk3}/lib:${pkgs.pango}/lib:${pkgs.glib}/lib:${pkgs.cairo}/lib"
    
    # Set pkg-config path
    export PKG_CONFIG_PATH="${pkgs.gtk3.dev}/lib/pkgconfig:${pkgs.pango.dev}/lib/pkgconfig:${pkgs.glib.dev}/lib/pkgconfig:${pkgs.cairo.dev}/lib/pkgconfig"

    # Clean up any existing virtual environment
    if [ -d "venv" ]; then
      echo "Removing existing virtual environment..."
      rm -rf venv
    fi
    
    # Initialize gsettings schema
    export GSETTINGS_SCHEMA_DIR="${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}/glib-2.0/schemas/"
    
    # Verify GTK is available
    echo "Testing GTK availability..."
    python -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" || echo "Warning: GTK not properly configured"
  '';
}
