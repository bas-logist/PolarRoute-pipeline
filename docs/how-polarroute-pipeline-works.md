# How PolarRoute-pipeline works

*PolarRoute-pipeline* creates one or more meshes using up-to-date source datasets. These meshes can then have optimised routes calculated upon them with optimisations such as fuel or traveltime.  

The logical flow of the pipeline is built from the [application.yaml](https://github.com/bas-logist/PolarRoute-pipeline/raw/main/application.yaml) config file, which details what tasks are to be performed and their dependencies. The pipeline resolves these dependencies and allows tasks to run in parallel, depending how many `WORKERS` have been defined in the [pipeline.yaml](https://github.com/bas-logist/PolarRoute-pipeline/raw/main/pipeline.yaml).  

If any task fails to complete successfully, it will raise an exception and prevent any future **dependencies** from executing.

## The workflow manager
The pipeline build command creates or re-creates from the `application.yaml` and `pipeline.yaml` a python script that is used by the [Jug](https://github.com/luispedro/jug) parallelisation package. The pipeline invokes 'Jug' with this python script for each `WORKER`, creating one or more parallel processes that can complete multiple tasks which being monitored. This collection of python script, 'Jug' and `WORKERS` is referred to as the 'workflow-manager'.  

Everything related to the workflow manager's operation is contained within the `<pipeline>/workflow-manager/` directory, which is created by the 'build' command.

## `pipeline.yaml`
This configuration file can be mostly left untouched other than the `MAXWORKERS` definition. The workflow manager will attempt to allocate **up to** this many workers to the pipeline.  
> Example:  
> **| You have 10 tasks the *could* all execute in parallel.**  
> **| You are using a platform that has 6 CPU threads.**  
>   * If you set `MAXWORKERS` to `2` the workflow manager will invoke 2 workers, meaning that the 2 CPU threads can complete all 10 tasks twice as quickly as if there was only 1 worker (i.e. 1 task done at a time).  
>   * If you set `MAXWORKERS` to `10` the workflow manager will invoke 10 workers but because this is more than available CPU threads there will be a significant amount of CPU context switching to achieve the effect of 10 CPU threads running. This results in slower performance.  
>   * If you set `MAXWORKERS` to `5` the workflow manager will invoke 5 workers, meaning that the 5 CPU threads can complete all 10 tasks five times as quickly as if there was only 1 worker (i.e. 1 task done at a time). This would also avoid CPU context switch and also leave 1 CPU thread free for the underlying platform.  

## `application.yaml`
### Environment variables
If the pipeline relies upon constants held within environment variables, these can be pre-defined under the `env:variables:` section of the yaml config file.  

Also note that the `PIPELINE_DIRECTORY` and `SCRIPTS_DIRECTORY` are mandatory for the pipeline to know where it is and where to look for the task scripts.  

### Task sequence
The sequence order and dependancies of the tasks (scripts) are defined under the `sequence:` section of the yaml config file.  

Each task (script) in the sequence has a `name:` and `depends:` field. The name is the name of the script to be found in the scripts directory. The depends can be either a single script name or a list of script names if there are multiple dependancies. If a script has no dependancy then the `depends:` field should contain an empty string `''`.  

***Currently shell scripts `.sh` and python scripts `.py` are the only supported task (script) names.*** 

Inspect the [application.yaml](https://github.com/bas-logist/PolarRoute-pipeline/raw/main/application.yaml) to show how the sequence of tasks can be constructed.  

## Logs
Logs of stderr and stdout are stored in `<pipeline>/logs/<config_name>_<date>.err` and `<pipeline>/logs/<config_name>_<date>.out` for debugging purposes.  

## Further detail
For more detail on the inner workings of the tasks PolarRoute-pipeline performs, please refer to the documentation for:  
 - [Jug](https://jug.readthedocs.io/en/latest/)  
 - [PolarRoute](https://antarctica.github.io/PolarRoute/)  
 - [MeshiPhi](https://antarctica.github.io/MeshiPhi/)  