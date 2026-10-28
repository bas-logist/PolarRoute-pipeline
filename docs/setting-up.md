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
PolarRoute-pipeline will need to use valid credentials to download DUACS products, ensure you have these set up as detailed below:

### Copernicus Marine API
The Copernicus API to is used to download up-to-date DUACS currents data. This service requires obtaining a USERNAME and PASSWORD for logging in. Once you have the username and password they can be stored separately to the pipeline in the user's `HOME` directory. You can register on the [Copernicus Marine API Registration](https://data.marine.copernicus.eu/register) page. Then, use the `copernicusmarine` command line tool to log in and set up your credentials file. First make sure that your python virtual environment is activated and you have installed the dependencies. Then:

``` bash
copernicusmarine login
# you will be prompted for your username and password and your credentials will be stored in a file at $HOME/.copernicusmarine/.copernicusmarine-credentials
```

Alternativey, Copernicus Marine credentials can be set using environment variables `COPERNICUSMARINE_SERVICE_USERNAME` and `COPERNICUSMARINE_SERVICE_PASSWORD` - these will be used in preference to the credentials file.

Now that everything is set up, the *PolarRoute-pipeline* can be used. Please refer to the [Using the pipeline](using.md) section of this documentation for details of how to operate the pipeline.

### GEBCO Bathymetry data
If you are running the pipeline locally, and do not have access to the BAS 
infrastructure (specifically the SAN), you can use the following script to
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

This is a large and static dataset, therefore you should only need to run this once.
