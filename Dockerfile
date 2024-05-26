FROM python:3-buster

ARG DEBUG="false"
WORKDIR /workspace
COPY . .

RUN \
    # debug
    id && \
    pwd && \
    echo $DEBUG && \
    # install packages
    apt update && \
    apt upgrade -y && \
    apt install -y sudo && \
    # create user `vscode`
    useradd docker -m && \
    mkdir -p /etc/sudoers.d/ && \
    echo docker ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/docker && \
    chmod 0440 /etc/sudoers.d/docker && \
    if [ "${DEBUG}" = "true" ] ; \
    # if in debug mode
    then pip install --disable-pip-version-check --no-cache-dir -r requirements-dev.txt ; \
    # if in production mode
    else pip install --disable-pip-version-check --no-cache-dir -r requirements.txt ; \
    fi ; 

EXPOSE 8000
#CMD ["uvicorn","app.main:app","--reload","--host=0.0.0.0"]