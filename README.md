# Architecture Lab
The repo provides examples to work with modern data-platform-architecture.

> A data platform serves as a unified system for efficiently managing and analyzing large
> datasets. It integrates components like databases, data lakes, and data warehouses to
> handle structured and / or unstructured data depending on the use cases.

[Anatomy of a Data Platform — How to choose your data architecture](https://medium.com/@lou_adam/anatomy-of-a-data-platform-how-to-choose-your-data-architecture-bc36472e7783)

[Jupyter](https://jupyter.org/) notebooks are used to create pipelines implementing a simplified **medallion architecture**

> A medallion architecture is a data design pattern used to logically organize data in a lakehouse,
> with the goal of incrementally and progressively improving the structure and quality of data as it
> flows through each layer of the architecture (from Bronze ⇒ Silver ⇒ Gold layer tables).\

[Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)


## Prerequisites

### Containers
The examples are provided as docker compose files. A working container setup with [docker](https://docs.docker.com/engine/install/) or [similar](https://podman.io/) is needed. From developer ergonomics perspective a decent shell is needed.

> [!NOTE]  
> **Docker**: The compose files where created on Linux with [docker-ce](https://docs.docker.com/engine/install/ubuntu/), tested on Windows with [Docker-Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) on Mac with [OrbStack](https://orbstack.dev/). Other container-environments like [podman](https://podman.io/) may work/may need adaptions.

### Shell
In a **Unix-like environments** like Mac/Linux typically a good shell is available out of the box (bash, zsh) in combination with a terminal (terminal, iTerm, Konsole, gnome-terminal, ...). 

For **Windows** a good combination of shell/terminal is [PowerShell](https://github.com/PowerShell/PowerShell)/[Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/). 

> [!NOTE]  
> **Powershell**: For windows users it might be necessary to set the execution-policy for powershell:

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

> [!WARNING]  
> **cmd.exe**: If you use [cmd.exe](https://en.wikipedia.org/wiki/Cmd.exe), you are without help. Nobody should use this old command-interpreter anymore!

### Python
A modern package manager for python should be used to simplify dependency-management and environment setup.

> [!NOTE]  
> **uv**: I very much recommend [uv](https://github.com/astral-sh/uv) "An extremely fast Python package and project manager, written in Rust."

## Examples
### 1_simple
Basic setup to work with [Jupyter](https://jupyter.org/) / [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)

### 2_storage_stream
Introduce [Apache Kafka](https://kafka.apache.org/) for streaming data and [MinIO](https://github.com/minio/minio) as a S3-compatible storage backend.

### 3_pipeline
Shows a simple data-pipeline with Bronze/Silver/Gold notebooks and storing data in [Parquet Format](https://parquet.apache.org/) and using [DuckDB](https://duckdb.org/) for data processing.

### 4_user_interface
A [streamlit](https://streamlit.io/) app to visualize the processed pipeline data in the **GOLD** layer. 