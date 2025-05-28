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
                pkgs = import nixpkgs { inherit system; };
                baseShell = essentials.devShells.${system}.python;
                doCheck = false;
                in {
                devShell = pkgs.mkShell {
                doCheck = false;
                name = "projeto-com-requests";
                buildInputs = baseShell.buildInputs ++ (with pkgs.python311Packages; [
# opencv4
                ]);

                shellHook = ''
                echo "Ambiente do projeto carregado (base Essentials + customizações)."
                ${baseShell.shellHook or ""}
                '';
                };
                });
} 
