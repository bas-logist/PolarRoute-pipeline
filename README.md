# PolarRoute-pipeline

PolarRoute-pipeline is a data pipeline used to automate the generation of ocean/sea-ice meshes and optimised routes for ocean vessel route-planning. This data pipeline forms part of the BAS Operational PolarRoute (OPR) project.

User documentation for PolarRoute-pipeline can be found [here](https://bas-amop.github.io/PolarRoute-pipeline/).

##  
  
## Basic process flow diagram of Operational PolarRoute
![Basic Process](docs/img/polarroute-basics.png)
  
PolarRoute-pipeline implements the first step (left-most) in the above diagram.

##  

## Installing the pipeline onto a HPC workstation

This pipeline uses the cylc workflow manager: https://cylc.github.io/

### Cloning and setting up installation directories

> [!NOTE]
> Make sure your cloned repo, directories, virtual environments, e.t.c are all
> in a directory path accessible to the slurm nodes.

1. **Log into the HPC workstation, change to a suitable location, and clone this repository**
   - `git clone https://github.com/bas-amop/PolarRoute-pipeline.git polarroute-pipeline`
   - Then move into the root of the directory.

2. **Create a Python virtual environment**
   The Python version must be **Python 3.9** or higher (3.12 was used during development).
   `uv` was used for the original project, so uv.lock and pyproject.toml are provided.

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


### Setting up cylc global configurations

You may be able to skip this step if you've set up a different cylc pipeline for HPC before.

1. Create a directory called 'flow', which will contain **cylc global configs**. These configs will apply to **every cylc pipeline** you run. 
   - E.g. the 'global.cylc' file defines PLATFORMS on which the pipeline can be run, under the section [platforms], and symlinks for processes. 

2. Set the environment variable CYLC_CONF_PATH to your flow directory: `setenv CYLC_CONF_PATH "/<your_path>/flow"`

> [!NOTE]
> By default, cylc will look for 'flow' in a hierarchy of locations including '/etc/cylc/flow/' and '~'. This default behaviour doesn't work well in cases where '~' is inaccessible to the nodes.

3. There's an `example_global.cylc` file in `PolarRoute-pipeline/flow`. Copy the file to the path you set in CYLC_CONF_PATH, and rename the copy to 'global.cylc'. Change it as follows:
   - Under 'global init-script', replace the value of 'HOME=' to your user space on the workstations.
   - Correct the CYLC_RUN_DIR to your local set-up. This should be the same as the path you set up in step 3.
   - Replace '<path_to_your_venv>/bin/activate' with your own virtual environment's activation path.
   - Under [install] [[symlink_dirs]] [[[slurm_platform]]] set 'run' to match CYLC_RUN_DIR.

4. In the terminal, type `cylc config` and check that the output matches your own global.cylc.
   - If it does, cylc is detecting your configuration.
   - If it doesn't, check that environment variable $CYLC_CONF_PATH is set correctly.


##  

# Setting up the pipeline

Even before the pipeline can be built for the first time, there are a number of one-time setup steps required.

1. Assuming you have already created a Python virtual environment and cloned this repository into a directory on a HPC Workstation or Local PC, move into the 'root' of the repository.  
`cd polarroute-pipeline`  

2. Create symbolic links for the venv **activation** script, **datastore** (where downloaded data products are to be stored), **logs**,  **outputs** (where the generated outputs are to be stored), **html** (for the summary status page) and **upload** + **push** (where outputs are copied to be sent shipside).
    - `ln -s <path-to-venv>/bin/activate <path-to-this-repo>/activate`
    - `ln -s <path-to-datastore> <path-to-this-repo>/datastore`
    - `ln -s <path-to-logs-directory> <path-to-this-repo>/logs`
    - `ln -s <path-to-output-archive> <path-to-this-repo>/outputs`
    - `ln -s <path-to-upload-directory> <path-to-this-repo>/upload`
    - `ln -s <path-to-push-directory> <path-to-this-repo>/push`
    - `ln -s <path-to-html-directory> <path-to-this-repo>/html`  

The links created above are specific to PolarRoute-pipeline as various data products are stored in differen't remote or local directories. If you are setting up a completely local instance of PolarRoute-pipeline then you could just create local folders within the pipeline directory, instead of links to external locations. Below is an explanation of why each link/directory is required:  

| Directory or Link | Purpose |
|--|--|
| `<pipeline>/activate` | So the pipeline knows which activation script to use |
| `<pipeline>/datastore` | Where to store and retrieve downloaded source datasets |
| `<pipeline>/logs` | Where to keep any log files |
| `<pipeline>/outputs` | Where to store and retrieve daily pipeline output products |
| `<pipeline>/upload` | Where to 'prepare' specific outputs before being sent |
| `<pipeline>/push` | Where to place any outputs to be sent. Specifically, the pipeline copies output products from the `upload` directory into the `push` directory. These are then picked up by an external synchronisation system which 'pulls' the products and automatically removes them from the `push` directory afterwards |
| `<pipeline>/html` | Where the pipeline publishes a static html summary page |

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

Now that everything is set up, the *PolarRoute-pipeline* can be used. Please refer to the [Using the pipeline](https://bas-amop.github.io/PolarRoute-pipeline/using) section of the user documentation for details of how to operate the pipeline.


# Behind the scenes

For information about how the pipeline works, please refer to the user documentation [How PolarRoute-pipeline works](https://bas-amop.github.io/PolarRoute-pipeline/how-polarroute-pipeline-works).
