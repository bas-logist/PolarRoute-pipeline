# Installing the pipeline

It is recommended to use a Python virtual environment to reduce the risk of any Python package conflicts.

This pipeline uses the cylc workflow manager: https://cylc.github.io/

## Cloning and setting up installation directories

> [!NOTE]
> Make sure your cloned repo, directories, virtual environments, e.t.c are all
> in a directory path accessible to the slurm nodes.

1. **Log into the HPC workstation, change to a suitable location, and clone this repository**
   - `git clone https://github.com/bas-logist/PolarRoute-pipeline.git polarroute-pipeline`
   - Then move into the root of the directory.

2. **Create a Python virtual environment**
   The Python version must be **Python 3.9** or higher (3.12 was used during development).

   - Check the available Python with `python --version`
   - If required, install or load a compatible python version. Your HPC administrator will be able to help with getting a compatible Python version.

3. **Activate the new newly created python venv**  
    - `source <path-to-venv>/bin/activate.csh`

> [!NOTE]
> Workstations use a non-bash shell, hence 'activate.csh' instead of 'activate'.

4. **Install requirements into the venv**
   - Use `python -m pip install -r requirements.txt` or the appropriate method for your favourite environment manager.

5. Create or choose an **installation directory** for your cylc pipelines. This needs to be different from where you've cloned your code.

> [!NOTE]
> By design, cylc tries to keep development and installed code separate. Cylc will create 'cylc-run' in this location when it installs.


## Setting up cylc global configurations

You may be able to skip this step if you've set up a different cylc pipeline for HPC before.
If you use a HPC such as JASMIN, cylc may be configured on there already. Consult the appropriate documentation.

If you're on a platform that doesn't have cylc installed on it, you can set things up like so:

1. Create a directory called 'flow', which will contain **cylc global configs**. These configs will apply to **every cylc pipeline** you run. 
   - The 'global.cylc' file defines platforms on which the pipeline can be run, under the section [platforms], and symlinks for processes. 

2. Set the environment variable CYLC_CONF_PATH to your flow directory: `setenv CYLC_CONF_PATH "/<your_path>/flow"`

> [!NOTE]
> By default, cylc will look for 'flow' in a hierarchy of locations including '/etc/cylc/flow/' and your home directory as accessed with '~'. This default behaviour doesn't work well in cases where your home directory is inaccessible to the nodes.

3. There's an `example_global.cylc` file in `PolarRoute-pipeline/flow`. Copy the file to the path you set in CYLC_CONF_PATH, and rename the copy to 'global.cylc'. Change it as follows:
   - Under 'global init-script', replace the value of 'HOME=' to your user space on the workstations.
   - Correct the CYLC_RUN_DIR to your local set-up. This should be the same as the path you set up in step 3.
   - Replace '<path_to_your_venv>/bin/activate' with your own virtual environment's activation path.
   - Under [install] [[symlink_dirs]] [[[slurm_platform]]] set 'run' to match CYLC_RUN_DIR.

4. In the terminal, type `cylc config` and check that the output matches your own global.cylc.
   - If it does, cylc is detecting your configuration.
   - If it doesn't, check that environment variable $CYLC_CONF_PATH is set correctly.


## Setting up download credentials
PolarRoute-pipeline will need to use valid credentials to download ERA5 and DUACS products, ensure you have these set up as detailed below:

### ERA5
The ERA5 downloader scripts make use of the CDS API (via the cdsapi python package) and require you to create a .cdsapirc file in your home directory ($HOME/.cdsapirc) containing a valid url and key for the API as described here: https://cds.climate.copernicus.eu/api-how-to  

From a shell:
``` bash
echo url: https://cds-beta.climate.copernicus.eu/api > $HOME/.cdsapirc
echo key: <your-unique-api-key> >> $HOME/.cdsapirc
echo verify:0 >> $HOME/.cdsapirc
```

### Copernicus Marine API
The Copernicus API to is used to download up-to-date DUACS currents data. This service requires obtaining a USERNAME and PASSWORD for logging in. Once you have the username and password they can be stored separately to the pipeline in the user's `HOME` directory. You can register on the [Copernicus Marine API Registration](https://data.marine.copernicus.eu/register) page.
``` bash
mkdir -p $HOME/.copernicusmarine
echo <your-unique-username> > $HOME/.copernicusmarine/user
echo <your-unique-password> > $HOME/.copernicusmarine/password
```
 - The above commands will create the required credentials files. If you wish to remove the details of these commands in your shell's history, you can perform the following:  
   1. Logout *(this will flush your shell history to ~/.bash_history)*
   1. Login
   1. ` cat /dev/null > ~/.bash_history ` *(this will erase all of your bash history)*


## Create or locate necessary directories

1. You will need the following directories: **datastore** (where downloaded data products are to be stored), **logs**,  **outputs** (where the generated outputs are to be stored), **html** (for the summary status page) and **upload** + **push** (where outputs are copied to be sent shipside).
   - If you are working in development: use `mkdir` to make these directories somewhere sensible in your testing environment. Do not put them inside these repo.
   - If you are working in production: work out the locations of these directories in your production environment.

Below is an explanation of why each link/directory is required:

| Directory or Link | Purpose |
|--|--|
| `<pipeline>/datastore` | Where to store and retrieve downloaded source datasets |
| `<pipeline>/logs` | Where to keep any log files |
| `<pipeline>/outputs` | Where to store and retrieve daily pipeline output products |
| `<pipeline>/upload` | Where to 'prepare' specific outputs before being sent |
| `<pipeline>/push` | Where to place any outputs to be sent. Specifically, the pipeline copies output products from the `upload` directory into the `push` directory. These are then picked up by an external synchronisation system which 'pulls' the products and automatically removes them from the `push` directory afterwards |
| `<pipeline>/html` | Where the pipeline publishes a static html summary page |


## Preparing PolarRoute-pipeline specific configurations

1. In your cloned repo, create a copy of 'example_environment.cylc' and name it to 'environment.cylc' (gitignored)

> [!NOTE]
> environment.cylc provides global environment variables to every step of PolarRoute-pipeline.

2. Inside 'environment.cylc', change the variables to ones that make sense for your current deployment.
Follow the guidance provided in the comments in that file.
   - Populate PYTHON_PATH with the path to Python in your PolarRoute-pipeline virtual enviroment
   - Populate DATASTORE through MOST_RECENT with the directories you found/made in 'Create or locate necessary directories'
   - Populate the COPERNICUS_* values with the credential files you made in 'Copernicus Marine API'
   - Populate ENVIRONMENT_CONFIGS and VESSEL_CONFIGS with the location of these files. Currently they are 
   under 'configs/environment_configs' and 'configs/vessel_configs' in this repository, but this is likely to change in the future.


Now that everything is set up, the *PolarRoute-pipeline* can be used. Please refer to the [Using the pipeline](https://bas-logist.github.io/PolarRoute-pipeline/using) section of the user documentation for details of how to operate the pipeline.
