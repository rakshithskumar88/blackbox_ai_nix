{ pkgs ? import <nixpkgs> {} }:

with pkgs.python3Packages;
buildPythonApplication {
  pname = "blackbox-ai";
  version = "0.1.0";
  src = ./.;

  buildInputs = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.pygobject3
    python3Packages.pycairo
    gtk3
    gobject-introspection
    gsettings-desktop-schemas
  ];

  propagatedBuildInputs = with pkgs.python3Packages; [
    pygobject3
    pycairo
  ];

  makeWrapperArgs = with pkgs; [
    "--prefix GI_TYPELIB_PATH : ${gtk3}/lib/girepository-1.0:${pango}/lib/girepository-1.0:${glib}/lib/girepository-1.0:${gobject-introspection}/lib/girepository-1.0"
    "--prefix LD_LIBRARY_PATH : ${gtk3}/lib:${pango}/lib:${glib}/lib:${cairo}/lib"
    "--prefix XDG_DATA_DIRS : ${gsettings-desktop-schemas}/share/gsettings-schemas/${gsettings-desktop-schemas.name}:${gtk3}/share/gsettings-schemas/${gtk3.name}"
  ];

  doCheck = false;

  meta = with pkgs.lib; {
    description = "A desktop AI assistant application for NixOS";
    homepage = "https://github.com/rakshithskumar88/blackbox_ai_nix";
    license = licenses.mit;
    platforms = platforms.linux;
  };
}
