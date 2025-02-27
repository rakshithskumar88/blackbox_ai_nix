{ pkgs ? import <nixpkgs> {} }:

with pkgs.python3Packages;
buildPythonApplication {
  pname = "blackbox-ai";
  version = "0.1.0";
  src = ./.;

  nativeBuildInputs = with pkgs; [
    gobject-introspection
    makeWrapper
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

  dontWrapGApps = true;

  preFixup = ''
    makeWrapperArgs+=(
      --prefix GI_TYPELIB_PATH : "${pkgs.gtk3}/lib/girepository-1.0"
      --prefix GI_TYPELIB_PATH : "${pkgs.pango}/lib/girepository-1.0"
      --prefix GI_TYPELIB_PATH : "${pkgs.glib}/lib/girepository-1.0"
      --prefix GI_TYPELIB_PATH : "${pkgs.gobject-introspection}/lib/girepository-1.0"
      --prefix XDG_DATA_DIRS : "${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}"
      --prefix XDG_DATA_DIRS : "${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}"
      --prefix GI_TYPELIB_PATH : "${pkgs.gobject-introspection}/lib/girepository-1.0"
      --prefix LD_LIBRARY_PATH : "${pkgs.gtk3}/lib"
      --prefix LD_LIBRARY_PATH : "${pkgs.pango}/lib"
      --prefix LD_LIBRARY_PATH : "${pkgs.glib}/lib"
      --prefix LD_LIBRARY_PATH : "${pkgs.cairo}/lib"
    )

    # Wrap the executable
    makeWrapper ${python.interpreter} $out/bin/blackbox-ai \
      --add-flags "-m blackbox_ai" \
      "''${makeWrapperArgs[@]}"
  '';

  postFixup = ''
    # Ensure the Python package is properly wrapped
    wrapPythonPrograms
  '';

  doCheck = false;  # Skip tests for now

  meta = with pkgs.lib; {
    description = "A desktop AI assistant application for NixOS";
    homepage = "https://github.com/rakshithskumar88/blackbox_ai_nix";
    license = licenses.mit;
    platforms = platforms.linux;
  };
}
