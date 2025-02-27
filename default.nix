{ pkgs ? import <nixpkgs> {} }:

with pkgs.python3Packages;
buildPythonApplication {
  pname = "blackbox-ai";
  version = "0.1.0";
  src = ./.;

  nativeBuildInputs = with pkgs; [
    wrapGAppsHook
    gobject-introspection
  ];

  buildInputs = with pkgs; [
    gtk3
    gobject-introspection
    cairo
    pango
    glib
    gsettings-desktop-schemas
  ];

  propagatedBuildInputs = with pkgs.python3Packages; [
    pygobject3
    pycairo
  ];

  # Enable GDK pixbuf loaders
  GDK_PIXBUF_MODULE_FILE = "${pkgs.librsvg}/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache";

  preFixup = ''
    gappsWrapperArgs+=(
      --prefix GI_TYPELIB_PATH : "${pkgs.gtk3}/lib/girepository-1.0"
      --prefix GI_TYPELIB_PATH : "${pkgs.pango}/lib/girepository-1.0"
      --prefix GI_TYPELIB_PATH : "${pkgs.glib}/lib/girepository-1.0"
      --prefix GI_TYPELIB_PATH : "${pkgs.gobject-introspection}/lib/girepository-1.0"
      --prefix XDG_DATA_DIRS : "${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}"
      --prefix XDG_DATA_DIRS : "${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}"
    )
  '';

  doCheck = false;  # Skip tests for now

  meta = with pkgs.lib; {
    description = "A desktop AI assistant application for NixOS";
    homepage = "https://github.com/rakshithskumar88/blackbox_ai_nix";
    license = licenses.mit;
    platforms = platforms.linux;
  };
}
