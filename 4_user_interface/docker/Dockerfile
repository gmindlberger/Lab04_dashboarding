FROM public.ecr.aws/docker/library/python:3.12-slim

ARG buildtime_variable_username="containeruser"
ARG buildtime_variable_groupname="containergroup"
ARG buildtime_variable_uid="65532"
ARG buildtime_variable_gid="65532"
ARG buildtime_application_dir="/opt/streamlit_dashboard"

WORKDIR ${buildtime_application_dir}

# 1) install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) copy streamlit app code
COPY src/dashboard .

RUN groupadd -r -g ${buildtime_variable_gid} ${buildtime_variable_groupname} \
 && useradd -rM -d ${buildtime_application_dir} -s /sbin/nologin \
      -g ${buildtime_variable_gid} -u ${buildtime_variable_uid} ${buildtime_variable_username} \
 && chown -R ${buildtime_variable_uid}:${buildtime_variable_gid} ${buildtime_application_dir}

USER ${buildtime_variable_username}

# 5) serve streamlit port
EXPOSE 8501

# 6) Entrypoint creation
RUN echo "#!/bin/bash\n\
streamlit run app.py \
  --server.port=8501 \
  --server.address=0.0.0.0" > entrypoint.sh \
 && chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
