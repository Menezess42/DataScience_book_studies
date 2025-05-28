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
                pkgs = import nixpkgs { inherit system;  config.doCheck = false;};
                baseShell = essentials.devShells.${system}.python;
                in {
                devShell = pkgs.mkShell {
                name = "projeto-com-requests";
                buildInputs = baseShell.buildInputs ++ [ #(with pkgs.python311Packages; [
                (pkgs.python311Packages.seaborn.overrideAttrs (old: {
                                                               doCheck = false;
                                                               }))
                                                               
                (pkgs.python311Packages.numpy.overrideAttrs (old: {
                                                               doCheck = false;
                                                               }))
                (pkgs.python311Packages.matplotlib.overrideAttrs (old: {
                                                               doCheck = false;
                                                               }))
                ];

                shellHook = ''
                echo "Ambiente do projeto carregado (base Essentials + customizações)."
                ${baseShell.shellHook or ""}
                '';
                };
                });
} 
