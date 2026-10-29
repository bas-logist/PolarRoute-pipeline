# PolarRoute-pipeline

PolarRoute-pipeline is a data pipeline used to automate the generation of ocean/sea-ice meshes and optimised routes for ocean vessel route-planning. This data pipeline forms part of the BAS Operational PolarRoute (OPR) project.

User documentation for PolarRoute-pipeline can be found [here](https://bas-logist.github.io/PolarRoute-pipeline/).

##  
  
## Basic process flow diagram of Operational PolarRoute
![Basic Process](docs/img/polarroute-basics.png)
  
PolarRoute-pipeline implements the first step (left-most) in the above diagram.

##  

## Installing the pipeline onto a HPC workstation

Please refer to the [Installation] (https://bas-logist.github.io/PolarRoute-pipeline/installation) section of the user documentation (nested under `docs`) for details of how to install the pipeline.

##

## Running PolarRoute-pipeline

See 'docs/using.md' for instructions on running PolarRoute-pipeline.


## File path design

Files are obtained from, and written to, a variety of different locations. Each directory is set in a variable to allow them to be changed between production and development. 

The directories group together files based on how frequently they change, e.g. rarely/daily/every run, and whether the files are temporary or push-ready. Accordingly, they will each have different rules around when and how often they are cleared.

Directories and their intended uses are as follows:

| Variable | Defined in | Change frequency | Persistent? | Purpose |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| DATASTORE  | environment.cylc | Daily | Yes | Stores downloaded reference files, e.g. from Copernicus, which may be reused by multiple pipeline runs in a single day. |
| ENVIRONMENTAL_CONFIGS | environment.cylc | Monthly/yearly | Yes | JSONs which defines which files in DATASTORE need loading and applying to each pipeline run, based on information such as region. |
| VESSEL_CONFIGS | environment.cylc |  Monthly/yearly | Yes | JSONs which set physical parameters of each vessel (1 vessel per file). |
| WAYPOINT_STATIC_CONFIGS | environment.cylc | Monthly/yearly | Yes | Static files for waypoints which rarely need changing, and are not updated by pipeline runs. |
| CYLC_WORKFLOW_SHARE_DIR | cylc built-in variable | Per run | **No** | Temporary location which is shared between all steps in 1 pipeline run. |
| CHECKPOINT | environment.cylc | Per run | Yes | Stores files which are computationally expensive to create from scratch. Optional skip-points in the pipeline allow you to start from these files, if they meet certain criteria. |
| STAGING | environment.cylc | Per **fully completed** run | Yes | Files in here are 'final' and ready to push. |
| PUSH | environment.cylc | Per **fully completed** run | Yes | The production location used by SIIS and PolarRoute-server. Integrity-checking data and sending it to this location is one of the *final* steps in the pipeline. |


## The structure of DATASTORE

The parent path of the 'datastore' can be varied, as seen in the previous section, but everything below it has a very set structure. This is because configuration files need to specify paths to each resource.


## Behind the scenes

For information about how the pipeline works, please refer to the user documentation [How PolarRoute-pipeline works](https://bas-logist.github.io/PolarRoute-pipeline/how-polarroute-pipeline-works).
