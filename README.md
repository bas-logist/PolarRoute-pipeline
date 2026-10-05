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

1. Activate your PolarRoute-pipeline virtual environment

2. Navigate to the polarroute-pipeline directory in the terminal, and check file validity: `cylc validate .` Follow up with any error messages you get.

3. If all is well, install the code to your 'run' directory: `cylc install`
   - It should give a result like mine: `INSTALLED PolarRoute-pipeline/run1 from /path/to/PolarRoute-pipeline`
   - It should be SYMLINKED in your specified run directory, under cylc-run. The 'original' will be in ~.

4. To run your pipeline on the HPC, and for the SDA vessel in the south region, use the following command. See 'Further configuration of the PolarRoute-pipeline' for details of how to add or remove vessels and regions:
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
