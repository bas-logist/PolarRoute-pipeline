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
   - `git clone https://github.com/bas-logist/PolarRoute-pipeline.git polarroute-pipeline`
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
If you use a HPC such as JASMIN, cylc may be configured on there already. Consult the appropriate documentation.

If you're on a platform that doesn't have cylc installed on it, you can set things up like so:

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


### Setting up download credentials
PolarRoute-pipeline will need to use valid credentials to download ERA5 and DUACS products, ensure you have these set up as detailed below:

#### ERA5
The ERA5 downloader scripts make use of the CDS API (via the cdsapi python package) and require you to create a .cdsapirc file in your home directory ($HOME/.cdsapirc) containing a valid url and key for the API as described here: https://cds.climate.copernicus.eu/api-how-to  

From a shell:
``` bash
echo url: https://cds-beta.climate.copernicus.eu/api > $HOME/.cdsapirc
echo key: <your-unique-api-key> >> $HOME/.cdsapirc
echo verify:0 >> $HOME/.cdsapirc
```

#### Copernicus Marine API
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


### Create or locate necessary directories

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


### Preparing PolarRoute-pipeline specific configurations

1. In your cloned repo, create a copy of 'example_environment.cylc' and name it to 'environment.cylc' (gitignored)

> [!NOTE]
> environment.cylc provides global environment variables to every step of PolarRoute-pipeline.

2. Inside 'environment.cylc', change the variables to ones that make sense for your current deployment.
Follow the guidance provided in the comments in that file.
   - Populate PYTHON_PATH with the path to Python in your PolarRoute-pipeline virtual enviroment
   - Populate DATASTORE through HTML with the directories you found/made in 'Create or locate necessary directories'
   - Populate the COPERNICUS_* values with the credential files you made in 'Copernicus Marine API'
   - Populate ENVIRONMENT_CONFIGS and VESSEL_CONFIGS with the location of these files. Currently they are 
   under 'configs/environment_configs' and 'configs/vessel_configs' in this repository, but this is likely to change in the future.


Now that everything is set up, the *PolarRoute-pipeline* can be used. Please refer to the [Using the pipeline](https://bas-logist.github.io/PolarRoute-pipeline/using) section of the user documentation for details of how to operate the pipeline.

##

## Running PolarRoute-pipeline

1. Activate your PolarRoute-pipeline virtual environment

2. Navigate to the polarroute-pipeline directory in the terminal, and check file validity: `cylc validate .` Follow up with any error messages you get.

3. If all is well, install the code to your 'run' directory: `cylc install`
   - It should give a result like mine: `INSTALLED PolarRoute-pipeline/run1 from /path/to/PolarRoute-pipeline`
   - It should be SYMLINKED in your specified run directory, under cylc-run. The 'original' will be in ~.

4. To run your pipeline for the HPC and the SDA vessel for central, north and south regions, use the following command. See 'Further configuration of the PolarRoute-pipeline' for details of how to add or remove vessels and regions:
   - `cylc play PolarRoute-pipeline/<run_number_at_install> \`
   `--set-file <your_run_directory>/cylc-run/PolarRoute-pipeline/<run_number_at_install>/set-files/hpc_defaults`

5. Track the progress of your pipeline like so:
   - `cylc scan --format=rich` will display progress from the point of view of the cylc process.
   - Check your **slurm queue** to see what jobs have been submitted by the pipeline.
   - Logs, output files, e.t.c. will all be viewable under: `<your_run_directory>/cylc-run/polarroute-pipeline/runNumber`. The most important ones, like slurm `.out` and `.err`, are in `<your_run_directory>/cylc-run/polarroute-pipeline/runNumber/log/job/<name_of_task>/01`

##

## Further configuration of the PolarRoute-pipeline

We provide a mandatory `--set-file` when we play the PolarRoute-pipeline. The set file specifies vital configuration settings. These are:
- SITE: The site argument is used to load **appropriate provisioning** for the platform you intend to use. When a site is provided, the pipeline finds a file with the same name in the `site` directory, and loads it. If you open `hpc_defaults` you can see that for many pipeline steps, it specifies maximum run time and memory.
- REGIONS_VESSELS: The regions_vessels argument specifies which regions and vessels need meshes, routes e.t.c. calculating for them. After some initial set-up, you can flexibly add or remove regions and vessels just by providing a new file, without a need to change the pipeline code.

### Worked examples: changes in resources and vessels

#### Changes in vessels and regions

Imagine it's far into the future and we have 2 boats, the SDA and the Raging Crustacean (RC). The SDA is touring the north and the RC is touring the south this year, with nothing needing information for the central region. Our HPC is unchanged.

The first time you work with a new vessel or region, you would need to make new configuration files. As these are stored in the repository, the process is not (yet) fully plug-and-play:
- Create an RC file in the `configs/vessel_configs` directory, using `SDA.config.json` to guide you.
- (If you had a new region) Create a region file in the `configs/environment_configs` directory, using existing files to guide you.

You'd then set up for the pipeline like so:
1. Create a new set file, specific to the current cruise plan.
2. Put the following in the set file and save it:
"""
SITE = "bas_hpc"
REGIONS_VESSELS = [{"region": "north", "vessel": "SDA"}, {"region": "south", "vessel": "RC"}]
"""
3. Run the cylc pipeline like so: `cylc play PolarRoute-pipeline/<run_number_on_deployment_install> \`
   `--set-file <wherever_you_saved_the_set_file>/<name_of_new_set_file>`

You may of course need to save the set file in an 'official' and documented location for live deployments, for auditability. 


#### Changes in HPC system

Imagine that we have an entirely new HPC system where the queues have different names.

1. Make a new file under `site`, with a unique name that is sensible for your system. It needs to end in `.cylc`
2. Use the existing `bas-hpc.cylc` file, and the documentation on portable workflows (https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/portable-workflows.html), to fill in your new file.
   - Make sure you encapsulate workflow steps in the Jinja2 {% for REGION_VESSEL in REGIONS_VESSELS %} {% endfor %} block. This will make sure that region/vessel selection flexibility continues to work.
3. Create a new set file where the SITE= is set to the unique name of your new system.
4. Run the cylc pipeline with the new set file.

The bit of `flow.cylc` that loads in the site files is right at the bottom of the document, with a link to the appropriate documentation:
```
{% include 'site/' ~ SITE ~ '.cylc' %}
```



# Behind the scenes

For information about how the pipeline works, please refer to the user documentation [How PolarRoute-pipeline works](https://bas-logist.github.io/PolarRoute-pipeline/how-polarroute-pipeline-works).
