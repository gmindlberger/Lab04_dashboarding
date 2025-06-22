# use the container-image built with spark 3.5.5
# https://github.com/bihe/architecture-lab/pkgs/container/architecture-lab%2Fjupyter_pyspark
FROM ghcr.io/bihe/architecture-lab/jupyter_pyspark:3.5.5
USER root

# setup necessary python packages
COPY requirements.txt .
RUN pip install --quiet --no-cache-dir -r ./requirements.txt

# we also need some additional java packages to work with spark, kafka and friends
COPY jars/kafka-clients-2.8.2.jar /usr/local/spark/jars
COPY jars/spark-sql-kafka-0-10_2.12-3.5.5.jar /usr/local/spark/jars
COPY jars/spark-token-provider-kafka-0-10_2.12-3.5.5.jar /usr/local/spark/jars
COPY jars/commons-pool2-2.12.1.jar /usr/local/spark/jars

USER $NB_UID