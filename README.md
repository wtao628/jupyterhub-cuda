<div align="center">
    <!--- Use <h1> because "#" doesn't work... --->
    <h1>Multi-Container JupyterHub</h1>
</div>

This is an example deployment of a multi-container JupyterHub. This JupyterHub
uses an extended version of the DockerSpawner to spawn single-user containers
with access to one GPU, provided one is available. These instructions apply to
Windows.

<h2>Prerequisites</h2>
To set up this JupyterHub, you will need to have installed:

<ul>
  <li><a href="https://docs.docker.com/desktop/install/windows-install/">Docker Desktop for Windows</a></li>
  <li><a href="https://apps.microsoft.com/detail/ubuntu-22-04-2-lts/9PN20MSR04DW?hl=en-us">Ubuntu</a> for WSL2</li>
  <li><a href="https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html">NVIDIA Container Toolkit</a> on Ubuntu for WSL2</li>
</ul>

<h2>Configure Docker Desktop</h2>
Prior to building the Dockerfile, Docker must be allowed to access the GPUs. To
do this:

<ol>
    <li>Navigate to the settings page for Docker Desktop and go to "Resources" > "WSL Integration";</li>
    <li>Check the option "Enable integration with my default WSL distro";</li>
    <li>Toggle on the integration with Ubuntu; and</li>
    <li>Click "Apply & restart".</li>
</ol>

You can check that the Docker Engine has access by running,

<code>docker run --rm --gpus all ubuntu nvidia-smi</code>

The output should be a table.

The JupyterHub also relies on a network. To create it, run:

<code>docker network create jupyternet</code>

<h2>Configuration</h2>
Depending on your situation, you may wish to make some changes. Some of the
configuration settings are in jupyterhub_config.py.

<h3>Changing the Authenticator</h3>
Currently, the authenticator is a dummy authenticator used for testing.

<h3>Number of GPUs</h3>
If your system has more than one GPU, go to the .env file and modify it
accordingly:

<ul>
    <li>If you have two GPUs, type <code>"01"</code>;</li>
    <li>If you have three GPUs, type <code>"012"</code>;</li>
    <li>and so on and so forth.</li>
</ul>

<h3>Modify the GPUDockerSpawner</h3>
If you want to modify the behavior of the <code>GPUDockerSpawner</code>, take
the wheel file and change the file extension to ".zip". Navigate to
"gpudockerspawner" > "gpudockerspawner.py" to make your changes.

<h3>Enabling HTTPS</h3>

Once you have finished modifying the files to your liking, run:

<code>docker compose up</code>
