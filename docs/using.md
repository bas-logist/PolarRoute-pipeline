# Running PolarRoute-pipeline

First install and set up, following the instructions in the 'installation.md' file in the docs.

## Running from the terminal

1. Activate your PolarRoute-pipeline virtual environment.

2. Navigate to the polarroute-pipeline directory.

3. Install the polarroute-pipeline code to your 'run' directory: `cylc install`
   - It should give a result like mine: `INSTALLED PolarRoute-pipeline/run1 from /path/to/PolarRoute-pipeline`
   - The install will go into ~ and be SYMLINKED to the $CYLC_RUN_DIR you set earlier

4. Create a 'set-file' to specify which SITE to use for computation, which REGIONS_VESSELS to run the pipeline for, and whether to apply a SKIP_OPTION. A set file looks like this:
```
SITE = "localhost"
REGIONS_VESSELS = [{"region": 'south', "vessel": "SDA"}]
SKIP_OPTION = "vessel"
```
The options:
| Variable name  | Options | Purpose |
| ------------- | ------------- | ------------- |
| SITE | String correponding to a file in 'sites' | Used to load appropriate resource settings for your current compute environment. A default one for working on a laptop is 'localhost' |
| REGIONS_VESSELS  | Python-style list-of-dictionaries, each with keys "region" and "vessel" | Specifies which combinations of regions and vessels the pipeline should be run for |
| SKIP_OPTION | One of: "none", "region", "vessel" | Whether to run the full pipeline (option "none"), skip the region mesh creation step (option "region"), or skip vessel mesh creation (option "vessel") |

   - See 'Worked examples of configuration of the PolarRoute-pipeline' for details of how to add or remove vessels and regions.

4. Run the pipeline with your set file:
   - `cylc play PolarRoute-pipeline/<run_number_at_install> \`
   `--set-file <fullpath-to-your-selected-set-file>`

5. Track the progress of your pipeline like so:
   - `cylc scan --format=rich` will display progress from the point of view of the cylc process.
   - Check your **slurm queue** to see what jobs have been submitted by the pipeline.
   - Logs, output files, e.t.c. will all be viewable under: `<your_run_directory>/cylc-run/polarroute-pipeline/runNumber`. The most important ones, like slurm `.out` and `.err`, are in `<your_run_directory>/cylc-run/polarroute-pipeline/runNumber/log/job/<name_of_task>/01`


##

## Worked examples of configuration of the PolarRoute-pipeline

Provided here are some examples to help you configure the pipeline for your needs.

### Worked examples: changes in resources and vessels

#### Changes in HPC system

You are using a HPC system where the queues have different names and attributes than the example given in [bas-hpc.cylc](../site/bas-hpc.cylc).

1. Make a new file under `site`, with a unique name that is sensible for your system. It needs to end in `.cylc`
2. Use the existing `bas-hpc.cylc` file, and the documentation on portable workflows (https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/portable-workflows.html), to fill in your new file.
   - Make sure you encapsulate workflow steps in the Jinja2 {% for REGION_VESSEL in REGIONS_VESSELS %} {% endfor %} block. This will make sure that region/vessel selection flexibility continues to work.
3. Create a new set file to provide at pipeline run time, where the SITE= is set to the unique name of your new system.
4. Run the cylc pipeline with the new set file.

The bit of `flow.cylc` that loads in the site files is right at the bottom of the document, with a link to the appropriate documentation:
```
{% include 'site/' ~ SITE ~ '.cylc' %}
```


#### Changes in vessels and regions

Imagine it's far into the future and you have 2 boats, the SDA and the Raging Crustacean (RC). The SDA is touring the north and the RC is touring the south this year, with nothing needing information for the central region.

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

