# Installing the pipeline

It is recommended to use a Python virtual environment to reduce the risk of any Python package conflicts.

This pipeline uses the cylc workflow manager: https://cylc.github.io/


## Cloning and setting up installation directories

> [!NOTE]
> If deploying on a HPC using slurm or similar, make sure your cloned repo, directories, virtual environments, e.t.c are all in a directory path accessible to the slurm nodes.

1. **Clone this repository**
   1. `git clone https://github.com/bas-logist/PolarRoute-pipeline.git polarroute-pipeline`
      - Then move into the root of the directory.

2. **Create a Python virtual environment**
      - The Python version must be **Python 3.9** or higher (3.12 was used during development).
      - Currently, the developers are using uv to manage virtual environments, and a pyproject.toml is provided.

3. **Activate the new newly created python venv**  
    - E.g. `source <path-to-venv>/bin/activate`

4. **Install requirements into the venv**
      - If using pip, change into the repository's root and run `pip install .`

5. Create or choose an **installation directory** for your cylc pipelines. This needs to be different from where you've cloned your code.
      - Before you run a cylc-pipeline for the first time, you run 'cylc install' on the code repository, which installs it to: your-installation-directory/cylc-run.
      - For a test run, your home directory is usually fine, as long as it's accessible to your planned compute resources.
      - For production, you should probably use the same installation location for every cylc pipeline.

> [!NOTE]
> By design, cylc tries to keep development and installed code separate.



## Setting up cylc global configurations

You may be able to skip this step if you've set up a different cylc pipeline for HPC before.
If you are using a HPC such as JASMIN, cylc may be configured on there already. Consult the appropriate documentation.

If you're on a platform that doesn't have cylc installed on it, you can set it up like so:

1. Create a directory called 'flow', which will contain **cylc global configs**. These configs will apply to **every cylc pipeline** you run. 
      - The 'global.cylc' file defines platforms on which the pipeline can be run, under the section [platforms], and symlinks for processes. 

2. Set the environment variable CYLC_CONF_PATH to your flow directory, e.g.: `setenv CYLC_CONF_PATH "/<your_path>/flow"`

> [!NOTE]
> By default, cylc will look for 'flow' in a hierarchy of locations including '/etc/cylc/flow/' and your home directory as accessed with '~'. This default behaviour doesn't work well in cases where your home directory is inaccessible to the nodes.

3. Create a `global.cylc` file to store global configurations. There's an `example_global.cylc` file in `PolarRoute-pipeline/flow`. Copy it to the path you set in CYLC_CONF_PATH, and rename the copy to 'global.cylc'. Change it as follows:
      - Under 'global init-script', replace the value of 'HOME=' to the path to your user space on your computing resource.
      - Correct the CYLC_RUN_DIR to the path you set in step 5 of `Cloning and setting up installation directories`, e.g. `/your/home/directory/cylc-run`
      - Replace '<path_to_your_venv>/bin/activate' with your own virtual environment's activation path.
      - Under the section [install] [[symlink_dirs]] [[[slurm_platform]]], set 'run' to match CYLC_RUN_DIR.

4. In the terminal, type `cylc config` and check that the output matches your own global.cylc.
      - If it does, cylc is detecting your configuration.
      - If it doesn't, check that environment variable $CYLC_CONF_PATH is set correctly and that the global.cylc file is in there.


## Setting up download credentials for downloaded products

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


## Obtaining larger static datasets 

### GEBCO Bathymetry data
The pipeline uses GEBCO gridded bathymetry data, but as this is a very large file, it does not install it automatically at this time. You can use the following script to
download and set up the [GEBCO gridded bathymetry data](https://www.gebco.net/data-products/gridded-bathymetry-data):

```shell
mkdir -p datastore/bathymetry/gebco && cd $_

# Make a request using wget - this can take a while to download
# as this bathymetry model can be greater than 7GB in size.
# Take note of the year here, newer versions may be available
wget -O gebco.zip https://www.bodc.ac.uk/data/open_download/gebco/gebco_2024/zip/

unzip gebco.zip
mv GEBCO_2024.nc gebco_global.nc

# Clean up, remove any unnecessary files
rm gebco.zip
rm *.pdf
```


## Configuring PolarRoute-pipeline

An 'environment.cylc' file is used to provide environment variables to the PolarRoute-pipeline.

1. In your cloned repo, create a copy of 'example_environment.cylc' and name it to 'environment.cylc' (gitignored)

2. Inside 'environment.cylc', change the variables to ones that make sense for your current deployment.
Follow the guidance provided in the comments in that file.
      - Populate PYTHON_PATH with the path to Python in your PolarRoute-pipeline virtual enviroment
      - DATASTORE through PUSH are directories which will be created to hold output data. The pipeline will create them if they don't exist already. Select appropriate paths.

      | Variable name  | Purpose |
      | ------------- | ------------- |
      | DATASTORE  | Stores datasets used in mesh calculation, such as DUACS datasets  |
      | CHECKPOINT  | Stores larger products, such as region and vessel meshes, which are needed if you re-run the pipeline using the 'skip' options |
      | STAGING  | A final storage location prior to push |
      | PUSH  | Where final products are uploaded |

      - Populate the COPERNICUS_* values with the credential files you made in 'Copernicus Marine API'
      - Populate ENVIRONMENTAL_CONFIGS and VESSEL_CONFIGS with the locations of these files. Currently they are 
      under 'configs/environment_configs' and 'configs/vessel_configs' in this repository, but this is likely to change in the future.


Now that everything is set up, the *PolarRoute-pipeline* can be used. Please refer to the [Using the pipeline](https://bas-logist.github.io/PolarRoute-pipeline/using) section of the user documentation for details of how to operate the pipeline.
