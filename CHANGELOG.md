# Changelog

Notable changes will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project aims to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased, version TBC]

### Added

- Add uv files for version management: uv.lock, pyproject, .python-version
- Add this changelog


### Removed

- Remove scripts which are replaced by runtime parameters (e.g. vessel_add_northern, mesh_generate_northern)


### Changed

- Convert the first section of the Jug pipeline to cylc:
  - Define the workflow in flow.cylc
  - Move files from `scripts` to cylc-compatible locations
  - Create example `environment.cylc` and `global.cylc` files, for setting configurations and paths
  - Create `site/bas_hpc.cylc`, for setting resource provisioning on your platform (localhost, Slurm, e.t.c.)
  - Create set-file, to provide vessels and regions at run-time
  - Change paths in scripts that are now set in the cylc environment
- Change the README to incorporate installation instructions specific to cylc


### Fixed

- NA


## [1.0.0]

- First release
