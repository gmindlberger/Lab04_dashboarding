# Spark with storage and streaming
The compose file defines a [spark](https://spark.apache.org/) setup with [jupyter](https://jupyter.org/) and introduces storage with [minio](https://min.io/) and streaming with [kafka](https://kafka.apache.org/).

- ✅ A Jupyter Notebook with PySpark preconfigured
- ✅ MinIO – An S3-compatible object storage for handling datasets
- ✅ Kafka – A message broker for streaming data

URLs:
- 📌 Jupyter Notebook: http://localhost:8888 (needs token, look in console-log)
- 📌 Spark UI: http://localhost:4040 (for active sessions)
- 📌 MinIO Console: http://localhost:9001 (User: admin, Password: password)
- 📌 Kafka Broker: localhost:9092


## 1. Start the environment
To start the necessary services use docker compose (or podman, or ...).

```bash
# uses the file compose.yaml|.yml by default
docker compose rm # remove old containers if available
docker compose up --build # start the spark environment and ensure container is built
```

The output is similar to this:

```
jupyter-spark  | Entered start.sh with args: start-notebook.py
jupyter-spark  | Running hooks in: /usr/local/bin/start-notebook.d as uid: 1000 gid: 100
jupyter-spark  | Done running hooks in: /usr/local/bin/start-notebook.d
jupyter-spark  | Running hooks in: /usr/local/bin/before-notebook.d as uid: 1000 gid: 100
jupyter-spark  | Sourcing shell script: /usr/local/bin/before-notebook.d/10activate-conda-env.sh
minio          | MinIO Object Storage Server
minio          | Copyright: 2015-2025 MinIO, Inc.
minio          | License: GNU AGPLv3 - https://www.gnu.org/licenses/agpl-3.0.html
minio          | Version: RELEASE.2025-04-08T15-41-24Z (go1.24.2 linux/amd64)
minio          | 
minio          | API: http://172.20.0.4:9000  http://127.0.0.1:9000 
minio          | WebUI: http://172.20.0.4:9001 http://127.0.0.1:9001  
minio          | 
minio          | Docs: https://docs.min.io
jupyter-spark  | Sourcing shell script: /usr/local/bin/before-notebook.d/10spark-config.sh
jupyter-spark  | Done running hooks in: /usr/local/bin/before-notebook.d
jupyter-spark  | Executing the command: start-notebook.py
jupyter-spark  | Executing: jupyter lab

[...]

jupyter-spark  | [C 2025-04-21 12:41:07.513 ServerApp] 
jupyter-spark  |     
jupyter-spark  |     To access the server, open this file in a browser:
jupyter-spark  |         file:///home/jovyan/.local/share/jupyter/runtime/jpserver-7-open.html
jupyter-spark  |     Or copy and paste one of these URLs:
jupyter-spark  |         http://localhost:8888/lab?token=b266e68134ba8768e8e8f6dc018086477919e05e6ef27184
jupyter-spark  |         http://127.0.0.1:8888/lab?token=b266e68134ba8768e8e8f6dc018086477919e05e6ef27184

```

## 2. Notebooks
The folder `notebooks` contains example notebooks to interact with the environment:
- *kafka_stream.ipynb*  --  Streaming query from Kafka topic
- *storage_minio.ipynb* --  Interact with the storage component MiniIO

To use the notebooks either the **Jupyter Web-UI** can be used ([http://localhost:8888](http://localhost:8888)) or the Jupyter server is connected in **VSCode** and notebooks opened within VSCode by using the URL with token ([http://localhost:8888/lab?token=<token-from-console>](http://localhost:8888/lab?token=<token-from-console>))

### Storage
The python package [boto3](https://pypi.org/project/boto3/) is available to interact with S3-compatible storage. The notebook example creates a bucket and puts a text-file in the bucket.

### Streaming
To use the kafka_stream notebook the Kafka topic needs to be available and messages need to be produced. To enable this scripts are available in the folder `src/scripts`.

- *kafka_create_topic*
- *kafka_console_producer*
- *kafka_console_consumer*

When the kafka notebook is executed, messages from the kafka are read and displayed directly in the notebook. 

![notebook output showing kafka stream](.images/notebook_kafka_output.png)


> [!NOTE]  
> **PowerShell**: The provided PowerShell scripts use the [current/modern PowerShell variant](https://github.com/PowerShell/PowerShell) and are not tested with the legacy PowerShell provided by Windows ([Differences between Windows PowerShell 5.1 and PowerShell 7.x](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell?view=powershell-7.5)).