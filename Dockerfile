# syntax=docker/dockerfile

FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

USER root

COPY gpudockerspawner-1.0.1-py3-none-any.whl .

# Set up Ubuntu and install JupyterHub
RUN apt-get update \
    && apt-get upgrade -y \
    # Reduce container size with --no-install-recommends flag
    && apt-get install -y --no-install-recommends nodejs npm python3 python3-pip \
    # Get rid of some files in /var/cache/apt/archives
    && apt-get clean \
    && npm install -g configurable-http-proxy \
    && npm cache clear --force \
    && python3 -m pip install -U setuptools pip \
    && python3 -m pip install dockerspawner jupyterhub notebook "oauthenticator[azuread]" gpudockerspawner-1.0.1-py3-none-any.whl \
    && mkdir /srv/jupyterhub /etc/jupyterhub \
    && rm gpudockerspawner-1.0.1-py3-none-any.whl

COPY jupyterhub_config.py /etc/jupyterhub

WORKDIR /root

# Set the secret as an environment variable which does not persist
RUN --mount=type=secret,id=password export PASSWORD=$(cat /run/secrets/password) \
    && echo root:${PASSWORD} | chpasswd

CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]