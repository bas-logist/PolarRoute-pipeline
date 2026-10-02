# Implementation

*PolarRoute-pipeline* is one of three broadly distinct components of the Operational PolarRoute (OPR) project.

1. **PolarRoute-pipeline ([this repo](https://github.com/bas-logist/PolarRoute-pipeline))**  
Required data products are downloaded, stored and processed shoreside where the data and compute resources are abundant. This generates ocean/sea-ice meshes (and routes if required) for areas of operational interest. These generated outputs are compressed and transferred via satellite (or other) link to shipside. PolarRoute-pipeline is built on the technologies of [PolarRoute](https://github.com/bas-logist/PolarRoute) and [MeshiPhi](https://github.com/bas-logist/MeshiPhi).

2. **PolarRoute-server**  
Once the meshes are available shipside they are ingested into an onboard database which allows them to be used to calculate optimised travel routes. These are calculated on demand and presented to the onboard user digitally. [PolarRoute-server](https://github.com/bas-logist/PolarRoute-server) handles the onboard mesh ingestion and route calculation through a command-line or graphical user interface.

3. **Sea-Ice-Information-System (SIIS)**  
The [SIIS](https://gitlab.data.bas.ac.uk/MAGIC/SIIS) front-end provides a graphical user interface whereby users can interact with Operational PolarRoute through a standard web browser.

From the three distinct components defined above, this documentation is concerned only with part (1.)  

## Basic process flow diagram
![Basic Process](img/polarroute-basics.png)

## Detailed process flow diagram
![Operational PolarRoute Process](img/pipeline_dfd.png)

## History
During 2024 the previous repository was manually ported from a hierarchy of bash and python scripts to an implementation using a workflow manager. The original scripts remained mostly unchanged although the introduction of the [Jug](https://jug.readthedocs.io/en/latest/) parallelisation package allowed the scripts to execute with strict dependency, monitoring and pipeline control. This was initially achieved using a handbuilt workflow manager script `operational-polarroute.py`.  
  
### September 2024 to October 2026
The workflow manager concept was rebuilt as a separate and generic workflow manager forming the package [simple-action-pipeline](https://github.com/antarctica/simple-action-pipeline). PolarRoute-pipeline was then ported to being a configuration of *simple-action-pipeline*.

### October 2026
The workflow manager was switched to [Cylc] (https://cylc.github.io/). This preserves dependency-based scheduling, control, and monitoring, while making it easier to switch configurations between sites and seasons, and benefitting from the larger community supporting this workflow manager.
