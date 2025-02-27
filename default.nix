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
    ninja
    librsvg
  ];

  dontWrapGApps = true;

  preFixup = ''
    makeWrapperArgs+=(
      "''${gappsWrapperArgs[@]}"
      --prefix GI_TYPELIB_PATH : "${pkgs.gtk3}/lib/girepository-1.0"
      --prefix GI_TYPELIB_PATH : "${pkgs.pango}/lib/girepository-1.0"
      --prefix GI_TYPELIB_PATH : "${pkgs.glib}/lib/girepository-1.0"
      --prefix GI_TYPELIB_PATH : "${pkgs.gobject-introspection}/lib/girepository-1.0"
      --prefix XDG_DATA_DIRS : "${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}"
      --prefix XDG_DATA_DIRS : "${pkgs.gtk3}/share/gsettings-schemas/${pkgs.gtk3.name}"
      --prefix PYTHONPATH : "$out/${pythonEnv.sitePackages}"
    )
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    mkdir -p $out/${pythonEnv.sitePackages}
    cp -r . $out/${pythonEnv.sitePackages}/blackbox_ai

    makeWrapper ${pythonEnv}/bin/python $out/bin/blackbox-ai \
      --add-flags "-m blackbox_ai" \
      "''${makeWrapperArgs[@]}"

    runHook postInstall
  '';
}
