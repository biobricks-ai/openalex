{
  description = "OpenAlex BioBrick";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
    dev-shell.url = "github:biobricks-ai/dev-shell";
  };

  outputs = { self, nixpkgs, flake-utils, dev-shell }:
    flake-utils.lib.eachDefaultSystem (system:
      with import nixpkgs { inherit system; };
      let
        pg2sqlite = stdenv.mkDerivation rec {
          pname = "pg2sqlite";
          version = "1.0.3";

          src = fetchurl {
            url =
              "https://github.com/caiiiycuk/postgresql-to-sqlite/releases/download/v${version}/${pname}-${version}.jar";
            sha256 = "sha256-s7ELwadymvZj3oBUH++OtiwswR5wf1j6izUN4Vz4OE8=";
          };

          buildInputs = [ makeWrapper jre ];

          dontBuild = true;
          dontUnpack = true;

          installPhase = ''
            mkdir -p $out/bin
            cp $src $out/pg2sqlite-${version}.jar
            makeWrapper ${jre}/bin/java $out/bin/pg2sqlite \
              --add-flags "-jar $out/pg2sqlite-${version}.jar"
          '';
        };
      in {
        devShells.default = mkShell {
          inputsFrom = [ dev-shell.devShells.${system}.default ];
          packages = [ pg2sqlite ];
        };
      });
}
