{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    pip
    pygobject3
    pycairo
  ]);
in
pkgs.stdenv.mkDerivation {
  name = "blackbox-ai";
  src = ./.;

  nativeBuildInputs = with pkgs; [
    wrapGAppsHook
    gobject-introspection
  ];

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
    librsvg
  ];

  dontBuild = true;  # Skip build phase
  dontConfigure = true;  # Skip configure phase

  installPhase = ''
    runHook preInstall

    mkdir -p $out/${pythonEnv.sitePackages}
    cp -r blackbox_ai $out/${pythonEnv.sitePackages}/

    mkdir -p $out/bin
    makeWrapper ${pythonEnv}/bin/python $out/bin/blackbox-ai \
      --set GI_TYPELIB_PATH "${pkgs.gtk3}/lib/girepository-1.0:${pkgs.pango}/lib/girepository-1.0:${pkgs.glib}/lib/girepository-1.0:${pkgs.gobject-introspection}/lib/girepository-1.0" \
      --set XDG_DATA_DIRS "${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}:${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}" \
      --prefix PYTHONPATH : "$out/${pythonEnv.sitePackages}" \
      --add-flags "-m blackbox_ai"

    runHook postInstall
  '';
}
