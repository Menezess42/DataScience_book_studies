{
    description = "Projeto Python com venv em flake";

    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
        flake-utils.url = "github:numtide/flake-utils";
        essentials.url = "git+file:///mnt/hdmenezess42/GitProjects/flakeEssentials";
    };

    outputs = { self, nixpkgs, flake-utils, essentials }:
        flake-utils.lib.eachDefaultSystem (system:
                let
                pkgs = import nixpkgs { inherit system; };
#python = pkgs.python311;
                pythonPkgs = pkgs.python311Packages;
                baseShell = essentials.devShells.${system}.python;
                in {
                devShell = pkgs.mkShell rec {
                name = "impurePythonEnv-flake";
                venvDir = "./.venv";

                buildInputs =[
                pythonPkgs.python
                pythonPkgs.venvShellHook
                pythonPkgs.numpy
                pythonPkgs.requests
                pythonPkgs.seaborn
                pkgs.taglib
                pkgs.openssl
                pkgs.libxml2
                pkgs.libxslt
                pkgs.libzip
                pkgs.zlib
                pkgs.git
                ] ++ baseShell.buildInputs;

# Install pip dependencies into the venv
                    # pip install -r requirements.txt
                postVenvCreation = ''
                    unset SOURCE_DATE_EPOCH
                    '';

# Allow pip install wheels
                postShellHook = ''
                    export NIX_BUILD_CORES=2
                    unset SOURCE_DATE_EPOCH
                    '';
                };
                }
                );
}
