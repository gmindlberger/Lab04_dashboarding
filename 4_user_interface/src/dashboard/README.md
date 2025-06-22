# Streamlit App Example

This is a very basic setup of a [streamlit](https://streamlit.io/) app. The application reads the files from the **Gold** layer of the medallion architecture and creates visualizations.

## Docker
A template docker `Dockerfile.template` file is available which can be used to create a customized version.

The values of defined parameters can be changed during docker build, or the default values can be changed.

**NOTE**: Within the `Dockerfile.template` a couple of `[TODO]` items highlight areas of change for the customized Dockerfile.

```docker
# INFO: args can be supplied via docker build
# they are used as a best-practise, that the docker image does not run using the root user
ARG buildtime_variable_username="containeruser"
ARG buildtime_variable_groupname="containergroup"
ARG buildtime_variable_uid="65532"
ARG buildtime_variable_gid="65532"

# [TODO] define your appliction woring directory
ARG buildtime_application_dir="/opt/streamlit_dashboard"
```

### Build & Run
Scripts are available to build the Dockerfile and run the Dockerfile
- docker_build (sh|powershell)
- docker_run (sh|powershell)


## Local python development
If you want to interact with the python logic locally a python interpreter is needed. The logic relies on python 3.12. It uses the awesome [uv package manager](https://docs.astral.sh/uv/).

- You can even use `uv` to install python: [https://docs.astral.sh/uv/guides/install-python/](https://docs.astral.sh/uv/guides/install-python/).
- Create a local `python venv`: [https://docs.astral.sh/uv/pip/environments/](https://docs.astral.sh/uv/pip/environments/)
- Manage `dependencies`: [https://docs.astral.sh/uv/concepts/projects/dependencies/](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- Sync `python packages`: [https://docs.astral.sh/uv/concepts/projects/sync/#syncing-the-environment](https://docs.astral.sh/uv/concepts/projects/sync/#syncing-the-environment)



### Working with uv:
```bash
# create a virtual-environment via uv
# doc: https://docs.astral.sh/uv/pip/environments/#using-python-environments
uv venv

# activate the environment
# linux/mac
source .venv/bin/activat
# windows
.venv\Scripts\activate

# add packages
uv add <package-name>

# sync with virtual-environment
uv sync
```


### Run the streamlit application
```bash
# note: streamlit needs to be installed
uv run streamlit run ./main.py
```
