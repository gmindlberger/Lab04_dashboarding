#!/bin/sh

# the MinIO image needs to run
# necessary files need to be available in the GOLD layer
# we need to use the same network where MinIO is located
docker run \
    --network lab-network \
    -e MINIO_ENDPOINT=http://minio:9000 \
    -p 8080:8080 \
    --name streamlit_dashboard \
    streamlit_dashboard