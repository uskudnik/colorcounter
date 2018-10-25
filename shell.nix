let channels = rec {
  pkgs = import <nixpkgs> {};
  pkgs-master = import (fetchTarball https://github.com/NixOs/nixpkgs/archive/master.tar.gz) {};
  #pkgs-unstable = import (fetchTarball https://nixos.org/channels/nixos-unstable/nixexprs.tar.xz) {};
};
in with channels;

let dependencies = rec {
  _python = pkgs.python36Full;
  _parallel = pkgs.parallel;
  _pip = pkgs.python36Packages.pip;
  _ipython = pkgs.python36Packages.ipython;
  _ipdb = pkgs.python36Packages.ipdb;
  _jupyter = pkgs.python36Packages.jupyter;
  _pipenv = pkgs-master.pipenv;
  
  _flake8 = pkgs.python36Packages.flake8;
  _pylint = pkgs.python36Packages.pylint;

  _pytest = pkgs.python36Packages.pytest;
  _pytaiohttp = pkgs.python36Packages.pytest-aiohttp;
  _pytasyncio = pkgs.python36Packages.pytest-asyncio;

  _numpy = pkgs.python36Packages.numpy;
  _matplotlib = pkgs.python36Packages.matplotlib;
  _scipy = pkgs.python36Packages.scipy;
  _pillow = pkgs.python36Packages.pillow;
  _numba = pkgs.python36Packages.numba;

  
  _aiohttp = pkgs.python36Packages.aiohttp;
  _aiodns = pkgs.python36Packages.aiodns;
  _aiofiles = pkgs.python36Packages.aiofiles;
  
  _argparse = pkgs.python36Packages.numba;
  _tqdm = pkgs.python36Packages.tqdm;
};
in with dependencies;

pkgs.stdenv.mkDerivation rec {
  name = "env";
  env = pkgs.buildEnv {
    name = name;
    paths = buildInputs;
  };

  buildInputs = [
    
    _pipenv
    _parallel

    (_python.buildEnv.override {
          ignoreCollisions = true;
          extraLibs = [
            _ipython
            _pipenv
            _ipdb
            _jupyter

            _pytest
            _pytaiohttp
            _pytasyncio

            _flake8
            _pylint

            _numpy
            _matplotlib
            _scipy
            _pillow
            _numba

            _aiohttp
            _aiodns
            _aiofiles

            _tqdm
            _argparse
          ];
        })
    
  ];

  shellHook = ''
      # set SOURCE_DATE_EPOCH so that we can use python wheels
      SOURCE_DATE_EPOCH=$(date +%s)
      BASE_PATH=$PWD
  
      # Create virtualenv if it doesn't exist already
      if [ ! -d $PWD/venv ]; then
        python3.6 -m venv venv
      fi

      export PATH=$PWD/venv/bin:$PATH
      export PYTHONPATH=$PWD:$PYTHONPATH
      source venv/bin/activate

      export PYTHONDONTWRITEBYTECODE=1

      pip install -r requirements.txt

      '';
}
