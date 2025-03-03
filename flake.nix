{
	description = "Day Planner and Investment Tracker";

	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
		flake-utils.url = "github:numtide/flake-utils";
	};

	outputs = { self, nixpkgs, flake-utils }:
		flake-utils.lib.eachDefaultSystem (system:
				let
				pkgs = import nixpkgs { inherit system; };
#enableIDE = true;
#idePackages = if enableIDE then import ./ide-packages.nix {inherit pkgs; } else [];
				in {
				devShell = pkgs.mkShell {                                                                  
				name = "day-planner-env";
				buildInputs = with pkgs; [
                python311
                # IDE Like Features
                pyright
                python311Packages.pip
                python311Packages.jedi
                python311Packages.jedi-language-server
                python311Packages.black
                python311Packages.flake8
                python311Packages.sentinel
                python311Packages.python-lsp-server
                python311Packages.virtualenv
                python311Packages.pyflakes  # Linter Pyflakes
                python311Packages.isort
                # Libs for the book
                python311Packages.matplotlib
				];                
				shellHook = ''                                                           
					echo "Welcome to the Day Planner and Investment Tracker environment!"                    
					'';                                                                                      
				};                                                                                         
				}
				);
}
