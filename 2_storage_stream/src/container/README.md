# Custom jupyter-pyspark container
[jupyter/docker-stacks](https://github.com/jupyter/docker-stacks.git) provides container images for different notebook variants and use-cases. To use a specific spark version one needs to have a look at the published images [quay.io/repository/jupyter/pyspark-notebook](https://quay.io/repository/jupyter/pyspark-notebook?tab=tags). Unfortunately there is no published image available for [spark-3.5.5](https://spark.apache.org/downloads.html) which is the current release (as of 2025-04-20).

But it is rather easy to create an image with a defined spark-version:

```bash
SPARK_VERSION=3.5.5
HADOOP_VERSION=3
OPENJDK_VERSION=17
BASE_IMAGE_NAME=jupyter_pyspark
IMAGE_NAME="${BASE_IMAGE_NAME}:${SPARK_VERSION}"

docker build --rm --force-rm \
    -t ${IMAGE_NAME} ./docker-stacks/images/pyspark-notebook \
    --build-arg openjdk_version=${OPENJDK_VERSION} \
    --build-arg spark_version=${SPARK_VERSION} \
    --build-arg hadoop_version=${HADOOP_VERSION} \
    --build-arg spark_download_url="https://archive.apache.org/dist/spark/"
```

Two scripts are available which **build** and **push** the created image to the github container-registry (`ghcr.io`)

- *docker_build_pyspark.sh* -- builds a docker-image with a given spark version
- *docker_push_pyspark.sh*  -- pushes the image to github [architecture-lab/packages](https://github.com/bihe?tab=packages&repo_name=architecture-lab)

> [!NOTE]  
> To push to [architecture-lab/packages](https://github.com/bihe?tab=packages&repo_name=architecture-lab) a [PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) is needed having the needed scopes.