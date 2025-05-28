# {
#     description = "Projeto que estende o ambiente Essentials";
#
#     inputs = {
#         nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
#         flake-utils.url = "github:numtide/flake-utils";
#         essentials.url = "git+file:///mnt/hdmenezess42/GitProjects/flakeEssentials";
#     };
#
#     outputs = { self, nixpkgs, flake-utils, essentials }:
#         flake-utils.lib.eachDefaultSystem (system:
#                 let
#                 pkgs = import nixpkgs { inherit system; };
#                 baseShell = essentials.devShells.${system}.python;
#                 in {
#                 devShell = pkgs.mkShell {
#                 name = "projeto-com-requests";
#
#                 buildInputs = baseShell.buildInputs ++ (with pkgs.python311Packages; [
# # opencv4
#                 numpy
#                 matplotlib
#                 seaborn
#                 ]);
#
#                 postShellHook = ''
#                 export NIX_BUILD_CORES=3
#                 '';
#
#                 shellHook = ''
#                 echo "Ambiente do projeto carregado (base Essentials + customizações)."
#                 ${baseShell.shellHook or ""}
#                 '';
#                 };
#                 });
# } 
{
  description = "Projeto Python com venv em flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python311;
        pythonPkgs = pkgs.python311Packages;
      in {
        devShell = pkgs.mkShell rec {
          name = "impurePythonEnv-flake";
          venvDir = ./.venv;

          buildInputs = with pythonPkgs; [
            # Python interpreter and venv support
            python
            venvShellHook

            # Nix-managed packages on PYTHONPATH
            numpy
            requests

            # Native libs for binary extensions
            taglib
            openssl
            libxml2
            libxslt
            libzip
            zlib
            git
          ];

          # Install pip dependencies into the venv
          postVenvCreation = ''
            unset SOURCE_DATE_EPOCH
            pip install -r requirements.txt
          '';

          # Allow pip install wheels
          postShellHook = ''
            unset SOURCE_DATE_EPOCH
          '';
        };
      }
    );
}
