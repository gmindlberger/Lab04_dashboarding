#!/bin/sh

# the MinIO image needs to run
# necessary files need to be available in the GOLD layer
# we need to use the same network where MinIO is located

docker run -d \
  --network lab-network \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=password \
  -v 3_pipeline_minio_data:/data \
  minio/minio:latest server /data --console-address ":9001"



#docker run \
#    --network lab-network \
#    -e MINIO_ENDPOINT=http://minio:9000 \
#    -p 8501:8501 \
#    --name streamlit_dashboard \
#    streamlit_dashboard