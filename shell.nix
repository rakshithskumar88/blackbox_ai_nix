{ pkgs ? import <nixpkgs> {} }:

let
  blackbox-ai = pkgs.callPackage ./default.nix {};
in
pkgs.mkShell {
  inputsFrom = [ blackbox-ai ];
  buildInputs = with pkgs; [
    blackbox-ai
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
    export GI_TYPELIB_PATH="${pkgs.gtk3}/lib/girepository-1.0:${pkgs.pango}/lib/girepository-1.0:${pkgs.glib}/lib/girepository-1.0:${pkgs.gobject-introspection}/lib/girepository-1.0"
    export XDG_DATA_DIRS="${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}:${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}:$XDG_DATA_DIRS"
    
    echo "Testing GTK availability..."
    python -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" || echo "Warning: GTK not properly configured"

    echo "Development environment ready. You can run the application with: blackbox-ai"
  '';
}
