FROM public.ecr.aws/docker/library/python:3.12-slim

ARG buildtime_variable_username="containeruser"
ARG buildtime_variable_groupname="containergroup"
ARG buildtime_variable_uid="65532"
ARG buildtime_variable_gid="65532"

WORKDIR /opt/weather_application

COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY ./kafka_weather_producer.py .

# Do not run as root user
## debian specific user/group creation
RUN groupadd -r -g ${buildtime_variable_gid} ${buildtime_variable_groupname} \
    && useradd -rM -d /opt/weather_application -s /sbin/nologin -g ${buildtime_variable_gid} -u ${buildtime_variable_uid} ${buildtime_variable_username}

RUN chown ${buildtime_variable_uid}:${buildtime_variable_gid} /opt/weather_application 

USER ${buildtime_variable_username}

CMD ["python", "/opt/weather_application/kafka_weather_producer.py"]