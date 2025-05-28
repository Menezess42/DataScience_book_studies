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
                                                               pytestCheckPhase="";
                                                               checkPhase = "";
                                                               }))
                                                               
                (pkgs.python311Packages.numpy.overrideAttrs (old: {
                                                               doCheck = false;
                                                               pytestCheckPhase="";
                                                               checkPhase = "";
                                                               }))
                (pkgs.python311Packages.matplotlib.overrideAttrs (old: {
                                                               doCheck = false;
                                                               pytestCheckPhase="";
                                                               checkPhase = "";
                                                               }))
                ];

                shellHook = ''
                echo "Ambiente do projeto carregado (base Essentials + customizações)."
                ${baseShell.shellHook or ""}
                '';
                };
                });
} 


{
  description = "Projeto que estende o ambiente Essentials e usa venv";

  inputs = {
    nixpkgs.url    = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    essentials.url = "git+file:///mnt/hdmenezess42/GitProjects/flakeEssentials";
  };

  outputs = { self, nixpkgs, flake-utils, essentials }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs      = import nixpkgs { inherit system; };
        pythonPkgs = pkgs.python311Packages;
        baseShell  = essentials.devShells.${system}.python;
      in {
        devShell = pkgs.mkShell rec {
          name    = "projeto-com-venv";
          # Diretório do venv
          venvDir = ".venv";

          buildInputs = [
            # Interpretador Python com suporte a venv
            pythonPkgs.python

            # Hook que cria e ativa o .venv antes de cair no shell
            pythonPkgs.venvShellHook

            # Dependências leves que queremos derivar pelo Nix
            pythonPkgs.numpy

            # Dependências do essentials (LSP, debug etc.)
          ] ++ baseShell.buildInputs;

          # Se precisar de libs nativas para compilar extensões pip
          nativeBuildInputs = with pkgs; [
            openssl
            zlib
            libxml2
            libxslt
            libzip
          ];

          # Após criar o .venv, instala tudo do requirements.txt via pip
          postVenvCreation = ''
            unset SOURCE_DATE_EPOCH
            pip install --upgrade pip
            pip install -r requirements.txt
          '';

          # Ajustes após entrar no shell
          postShellHook = ''
            # Exportar variável se necessário em runtime
            echo "Ambiente (Essentials + venv Python) pronto."
          '';

          # Mantém seu shellHook original do Essentials
          shellHook = ''
          export NIX_BUILD_CORES=2
            ${baseShell.shellHook or ""}
          '';
        };
      });
}
