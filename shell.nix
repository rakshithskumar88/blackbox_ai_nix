{ pkgs ? import <nixpkgs> {} }:

let
  blackbox-ai = pkgs.callPackage ./default.nix {};
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.pygobject3
    python3Packages.pycairo
    gtk3
    gobject-introspection
    cairo
    pango
    glib
    gsettings-desktop-schemas
  ];

  shellHook = ''
    # Set up GObject Introspection paths
    export GI_TYPELIB_PATH="${pkgs.gtk3}/lib/girepository-1.0:${pkgs.pango}/lib/girepository-1.0:${pkgs.glib}/lib/girepository-1.0:${pkgs.gobject-introspection}/lib/girepository-1.0"
    
    # Set up library paths
    export LD_LIBRARY_PATH="${pkgs.gtk3}/lib:${pkgs.pango}/lib:${pkgs.glib}/lib:${pkgs.cairo}/lib"
    
    # Set up GSettings schemas
    export XDG_DATA_DIRS="${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}:${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}:$XDG_DATA_DIRS"
    
    # Set up pkg-config path
    export PKG_CONFIG_PATH="${pkgs.gtk3.dev}/lib/pkgconfig:${pkgs.pango.dev}/lib/pkgconfig:${pkgs.glib.dev}/lib/pkgconfig:${pkgs.cairo.dev}/lib/pkgconfig"

    # Verify GTK is available
    echo "Testing GTK availability..."
    python -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" || echo "Warning: GTK not properly configured"

    echo "Development environment ready. You can run the application with: python -m blackbox_ai"
  '';
}
