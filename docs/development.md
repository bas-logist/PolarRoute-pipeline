# Development

Depends on:

* Python >=3.9

---

1. Clone the repository and create and activate a python virtual environment of your choice.
2. Change into the repository directory. If using pip, install requirements from the `pyproject.toml` using `pip install .`

## Release/Versioning

Version numbers should be used in tagging commits on the `main` branch and should be of the form `v0.1.7` using the semantic versioning convention.

## Building & deploying the documentation

The documentation should build automatically on pushes to `main` using GitHub actions, if you want to build and deploy the docs manually, follow these steps:

* Run `make build-docs` to build the docs to the `./site` directory.
* Then run `make deploy-docs` to deploy to the `gh-pages` branch of the repository. You must have write access to the repo.