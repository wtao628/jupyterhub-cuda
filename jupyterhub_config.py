"""Configuration file for JupyterHub."""

import os

from gpudockerspawner import GPUDockerSpawner
from jupyterhub.spawner import Spawner


def cpu_limit(spawner: Spawner) -> float:
    """
    Allocates a single core to a user unless otherwise specified.

    Parameters
    ----------
    spawner : Spawner
        The spawner that creates the single-user JupyterHub containers.

    Returns
    -------
    float
        The amount of CPU cores allocated to the user.
    """
    user_allocation = {}
    return user_allocation.get(spawner.user.name, 1)


def display_gpu_images(spawner: Spawner) -> 'dict[str, str]':
    """
    Determines if the GPU-accelerated notebooks should be shown to the user.

    Parameters
    ----------
    spawner : Spawner
        The spawner that creates the single-user JupyterHub containers.

    Returns
    -------
    dict
        The single-user container images that can be selected.
    """
    if os.environ["GPUS"] != "":
        return {"CUDA Notebook": "gpu-notebook",
                "Standard Notebook": "stnd-notebook"}
    else:
        return {"Standard Notebook": "stnd-notebook"}


def mem_limit(spawner: Spawner) -> str:
    """
    Allocates two gigabytes of memory to a user unless otherwise specified.

    Parameters
    ----------
    spawner : Spawner
        The spawner that creates the single-user JupyterHub containers.

    Returns
    -------
    string
        The amount of memory allocated to the user.
    """
    user_allocation = {}
    return user_allocation.get(spawner.user.name, "2G")

# %% Configuration settings
c = get_config()

# Use for testing only!
c.JupyterHub.authenticator_class = "dummy"

# Spawn single-user containers with DockerSpawner
c.JupyterHub.spawner_class = GPUDockerSpawner

# Set CPU and memory limits
c.GPUDockerSpawner.cpu_limit = cpu_limit
c.GPUDockerSpawner.mem_limit = mem_limit

# Spawn containers from these images
c.GPUDockerSpawner.allowed_images = display_gpu_images
c.GPUDockerSpawner.gpu_notebooks = ["gpu-notebook"]

# Listen on all IPs when Hub is in a container
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_connect_ip = "jupyterhub"

# Connect containers to Docker network
c.GPUDockerSpawner.use_internal_ip = True
c.GPUDockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]

# Persist notebook directory on volume
notebook_dir = "/home/ubuntu"
c.GPUDockerSpawner.notebook_dir = notebook_dir
c.GPUDockerSpawner.default_url = "/lab"
c.GPUDockerSpawner.args = [f"--NotebookApp.notebook_dir={notebook_dir}"]
c.GPUDockerSpawner.volumes = {"jupyterdata-{username}": notebook_dir}

# Stop container once user logs out
c.JupyterHub.shutdown_on_logout = True

# Remove containers once they are stopped
c.GPUDockerSpawner.remove = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080
