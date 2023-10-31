{
  description = "OpenAlex BioBrick";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
    dev-shell.url = "github:biobricks-ai/dev-shell";
  };

  outputs = { self, nixpkgs, flake-utils, dev-shell }:
    flake-utils.lib.eachDefaultSystem (system:
      with import nixpkgs { inherit system; }; {
        devShells.default = mkShell {
          inputsFrom = [ dev-shell.devShells.${system}.default ];
          packages = [
            /* Problem: awscli uses Python which causes an issue with using
             * biobricks Python installed outside of shell
             */
            #awscli
          ];
        };
      });
}
