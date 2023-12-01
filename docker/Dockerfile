# Base image
FROM ubuntu:latest

# Update Debian packages and install system dependencies
RUN apt-get update && \
	apt-get install -y wget bzip2 && \
	apt-get install -y git

# Clone application code from the remote repository on GitHub
RUN git clone https://github.com/HassanMahmoodKhan/Remote-Health-Monitoring.git

# Download and install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Set the environment variable
ENV PATH /opt/conda/bin:$PATH

# Create a Conda environment
COPY environment_linux.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && \
    rm /tmp/environment.yml

# Set the default shell to Bash
SHELL ["/bin/bash", "-c"]

# Activate the Conda environment
ENV BASH_ENV ~/.bashrc
RUN conda init bash

# Open a bash terminal
CMD ["bash"]