# How PolarRoute-pipeline works

*PolarRoute-pipeline* creates one or more meshes using up-to-date source datasets. These meshes can then have optimised routes calculated upon them with optimisations such as fuel or traveltime.  


## The workflow manager

The pipeline is written in the [Cylc workflow engine] (https://cylc.github.io/), and uses cylc's syntax. A pipeline is 'installed' to a non-repo location, and then 'played', or run. 

Cylc pipelines can run on HPCs and on local machines/VM. In production, PolarRoute-pipeline is intended to be used in a VM, but it can be run on a Slurm queue on HPC during testing.

It's worth getting familiar with cylc before installing the pipeline, if you haven't used it before. The documentation is linked [here] (https://cylc.github.io/cylc-doc/stable/html/index.html), and there is a useful tutorial too.


### Core pipeline logic

The logical flow of the pipeline is laid out in the [flow.cylc](https://github.com/bas-logist/PolarRoute-pipeline/flow.cylc) workflow file. 

The `graph` section details which details what tasks are to be performed, and their dependencies. The pipeline resolves dependencies and allows tasks to run in parallel where appropriate. If any task fails to complete successfully, it will raise an exception and prevent any future **dependencies** from executing.

The details of the tasks are written in subheadings under the `runtime` section. For cylc, these largely consist of the script which is run, and any task-specific environmental variables that need to be set before running. Python scripts are stored in [/lib/python] (https://github.com/bas-logist/PolarRoute-pipeline/lib/python) and bash scripts are stored in [/bin] (https://github.com/bas-logist/PolarRoute-pipeline/bin). Currently, the environment variable lists are longer than strictly needed, because global variables defined in `environment.cylc` (see next section) don't need to be entered again. This is a design choice to try to improve clarity.

As an example: `data_retrieve_amsr` appears in the graph, showing that `check_active_hours` won't run until both `data_retrieve_amsr` and `data_subset_duacs` have completed: `data_subset_duacs & data_retrieve_amsr => check_active_hours`. Under `runtime`, a `[[data_retrieve_amsr]]` sub-headed section tells us that the pipeline job must run `data_retrieve_amsr.sh`, and pass it a list of environment variables, like the resource URL `AMSR_URLS_NORTH_START`.

### Setting up
#### Set how cylc runs on your computer

If you haven't run cylc on a computer/platform before, you'll need to install it and set up generic global arguments to ensure it behaves correctly. See `Setting up cylc global configurations` in the README.

#### Setting environment variables for PolarRoute-pipeline

Global environment variables, e.g. the file paths for datastore directories, are set in an `environment.cylc` file, which should be gitignored. See [example_environment.cylc] (https://github.com/bas-logist/PolarRoute-pipeline/example_environment.cylc) for guidance on what needs to be filled out.

You can create a different `environment.cylc` file for every platform you run a pipeline on, or use them to try out different production and testing set-ups easily.

#### Influence PolarRoute-pipeline logic with the set-file

Passing a set-file at runtime allows you to flexibly change:
- The site you're running the pipeline on, which affects provisioning, e.g. local laptop or HPC
- Which regions and vessels you want meshes to be created for
- Whether you want specific steps to be skipped (e.g. it's possible to skip region mesh creation, if an up-to-date mesh exists)

Set files are stored in a [set-file] (https://github.com/bas-logist/PolarRoute-pipeline/set-files) directory.

#### Configuring PolarRoute-pipeline provisioning

Provisioning is separated from tasks, to make the pipeline more portable. Provisioning information is written in a `my_site.cylc` file in the [site] (https://github.com/bas-logist/PolarRoute-pipeline/site) directory, where `my_site` is substituted with an appropriate name for your run location - for example, 'bas_hpc' for the BAS HPC, or 'local_defaults' for your personal laptop.

When you play the pipeline, you pass a set file (see [set-file] (https://github.com/bas-logist/PolarRoute-pipeline/set-files) for examples) which will contain the name of your site. This makes the pipeline load the correct provisioning information for your resource.


## Running the pipeline

- Activate your virtual environment first. `uv` is recommended and a `uv.lock` file is provided.
- Run `cylc install` in the cloned repository directory, to install your pipeline to the location set in the cylc global configuration. Note the run number assigned to this install, e.g. PolarRoute-pipeline/run1
- To run the installed pipeline with a set file, use the following command, substituting the run number and the set file name for correct ones: `cylc play PolarRoute-pipeline/run1 --set-file /path/to/set/file`
- `cylc scan` will briefly show pipelines that are running. `cylc scan --format=rich` is more verbose.
- If running on a slurm queue, use `squeue -u your_username` to see which jobs are currently running.


## Cylc outputs

### Overview 

Important files are saved to locations specified in the environment.cylc file and in flow.cylc. Other cylc outputs are saved in standardised way. Some useful files and directories are as follows. Substitute the actual name of a task, e.g. `data_retrieve_amsr`, for `task_name`.

#### The bash file **actually** run by cylc
Can be useful in trouble-shooting.
See under: `/install_location/polarroute-pipeline/runN/.service/etc/job.sh`

#### Temporary files produced during pipeline run
Can be useful in trouble-shooting.
See under `/install_location/PolarRoute-pipeline/runN/work/1/task_name`.

#### Log files, including stderr and stdout
- `job.err` and `job.out` - stderr and stdout for each task, stored under `/install_location/PolarRoute-pipeline/runN/log/job/1/task_name`
- If you have configurations that don't seem to be loading, you can double check here: `/install_location/PolarRoute-pipeline/runN/log/config/`


## Further details

For more detail on the inner workings of the tasks PolarRoute-pipeline performs, please refer to the documentation for:  
 - [PolarRoute](https://antarctica.github.io/PolarRoute/)  
 - [MeshiPhi](https://antarctica.github.io/MeshiPhi/)  