{
  description = "Projeto que estende o ambiente Essentials";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    essentials.url = "git+file:///mnt/hdmenezess42/GitProjects/flakeEssentials";
  };

  outputs = { self, nixpkgs, flake-utils, essentials }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # Overlay local que desativa o checkPhase nos pacotes Python
        pythonOverlay = final: prev: {
          python311 = prev.python311.override {
            packageOverrides = pyself: pysuper: {
              buildPythonPackage = args: pysuper.buildPythonPackage (args // {
                doCheck = false;
                checkPhase = "echo 'checkPhase desativado por flake.'";
              });
            };
          };
        };

        pkgs = import nixpkgs {
          inherit system;
          overlays = [ pythonOverlay ];
        };

        baseShell = essentials.devShells.${system}.python;

      in {
        devShell = pkgs.mkShell {
          name = "projeto-com-requests";

          buildInputs = baseShell.buildInputs ++ (with pkgs.python311Packages; [
            requests
            # opencv4  # descomentável se necessário
          ]);

          shellHook = ''
            echo "Ambiente do projeto carregado (base Essentials + customizações)."
            ${baseShell.shellHook or ""}
          '';
        };
      });
}
#
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
#                 ]);
#
#                 shellHook = ''
#                 echo "Ambiente do projeto carregado (base Essentials + customizações)."
#                 ${baseShell.shellHook or ""}
#                 '';
#                 };
#                 });
# } 
