
{
  description = "Projeto que estende o ambiente Essentials, sem pytestCheckPhase";

  inputs = {
    nixpkgs.url       = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url   = "github:numtide/flake-utils";
    essentials.url    = "git+file:///mnt/hdmenezess42/GitProjects/flakeEssentials";
  };

  outputs = { self, nixpkgs, flake-utils, essentials }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # 1) Define o overlay que desliga todos os checks nos pacotes Python:
        disablePythonChecks = final: prev: {
          buildPythonPackage = prev.buildPythonPackage.overrideAttrs(old: {
            doCheck   = false;
            checkPhase = ''
              echo "## pytestCheckPhase SKIPPED ##"
            '';
          });
        };

        # 2) Importa nixpkgs aplicando o overlay:
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ disablePythonChecks ];
          # opcional: config.doCheck = false;  # reforço global, mas não obrigatório com o overlay
        };

        # 3) Puxa o devShell do seu flake “essentials”
        baseShell = essentials.devShells.${system}.python;
      in
      {
        devShell = pkgs.mkShell {
          name = "projeto-com-requests";

          buildInputs = baseShell.buildInputs ++ (with pkgs.python311Packages; [
            opencv4
            # … outros pacotes Python
          ]);

          shellHook = ''
            echo "Ambiente do projeto carregado (base Essentials + customizações)."
            ${baseShell.shellHook or ""}
          '';
        };
      }
    );
}
