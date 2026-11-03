# Installing the pipeline

It is recommended to use a Python virtual environment to reduce the risk of any Python package conflicts.

### HPC Workstation or Local PC

1. **Create a Python virtual environment**  
   The Python version must be **Python 3.9** or higher (3.12 was used during development).
    
    - Check the available Python with `python --version`
    - If required, install or load a compatible python version. Your HPC administrator will be able to help with getting a compatible Python version.
    - then `python -m venv <path-to-venv>` with a path of your choosing.

1. **Source the new newly created python venv**  
    - `source <path-to-venv>/bin/activate` (Assuming you're using Bash or similar. Use the appropriate activate script within that folder depending on your shell)

1. **Clone this repository**
    - Assuming you have already cloned this repository into a directory, move into the 'root' of this repository. `cd polarroute-pipeline`.
    - Otherwise `git clone https://github.com/bas-logist/PolarRoute-pipeline.git polarroute-pipeline`
    - then `cd polarroute-pipeline`

1. **Install requirements**  
    - Using python pip (inside the created venv) `python -m pip install -r requirements.txt`

