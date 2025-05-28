{
  description = "Projeto que estende o ambiente Essentials";

  inputs = {
    nixpkgs.url     = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    essentials.url = "git+file:///mnt/hdmenezess42/GitProjects/flakeEssentials";
  };

  outputs = { self, nixpkgs, flake-utils, essentials }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # overlay que desativa todos os pytest nos python311Packages
        disableAllPythonChecks = final: prev: {
          python311Packages = prev.python311Packages.overrideScope (self: super: {
            inherit (builtins.listToAttrs
              (map (p: {
                name  = p;
                value = super.${p}.overrideAttrs (old: { doCheck = false; });
              })
              (builtins.attrNames super)
            ));
          });
        };

        pkgs = import nixpkgs {
          inherit system;
          config.doCheck = false;       # ainda bom manter
          overlays = [ disableAllPythonChecks ];
        };

        # agora esse baseShell já vem com pytest desligado em todo python311Packages
        baseShell = essentials.devShells.${system}.python;
      in {
        devShell = pkgs.mkShell {
          name = "projeto-com-requests";
          buildInputs = baseShell.buildInputs;
          shellHook   = ''
            echo "Ambiente carregado!"
            ${baseShell.shellHook or ""}
          '';
        };
      }
    );
}

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
#                 pkgs = import nixpkgs { inherit system;  config.doCheck = false;};
#                 baseShell = essentials.devShells.${system}.python;
#                 in {
#                 devShell = pkgs.mkShell {
#                 name = "projeto-com-requests";
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
