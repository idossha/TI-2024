
# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variables for non-interactive apt-get installs
ENV DEBIAN_FRONTEND=noninteractive
ENV SIMNIBS_VERSION=4.1.0
ENV SIMNIBS_INSTALLER=simnibs_installer_linux.tar.gz
ENV PATH=/opt/conda/bin:$PATH

# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variables for non-interactive apt-get installs
ENV DEBIAN_FRONTEND=noninteractive
ENV SIMNIBS_VERSION=4.1.0
ENV SIMNIBS_INSTALLER=simnibs_installer_linux.tar.gz
ENV PATH=/opt/conda/bin:$PATH

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies and tools
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    git \
    bc \
    jq \
    software-properties-common \
    libglu1-mesa \
    libxi6 \
    libxmu6 \
    libxrender1 \
    libxtst6 \
    libxft2 \
    libfreetype6 \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Copy environment file and create environment
COPY environment_linux.yml .
RUN /opt/conda/bin/conda env create -f environment_linux.yml -c conda-forge

# Install FSL
RUN wget -qO- https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py | python3 -c "import sys; exec(sys.stdin.read())" && \
    echo "FSLDIR=/usr/local/fsl" >> ~/.bashrc && \
    echo "PATH=\${FSLDIR}/bin:\${PATH}" >> ~/.bashrc && \
    echo "export FSLDIR PATH" >> ~/.bashrc

# Install SimNIBS
RUN wget https://github.com/simnibs/simnibs/releases/download/v${SIMNIBS_VERSION}/${SIMNIBS_INSTALLER} && \
    tar -xzf ${SIMNIBS_INSTALLER} -C /opt && \
    rm ${SIMNIBS_INSTALLER} && \
    echo "PATH=/opt/simnibs-${SIMNIBS_VERSION}/bin:\$PATH" >> ~/.bashrc

# Ensure the necessary environment variables for FreeSurfer
RUN echo "export FREESURFER_HOME=/opt/simnibs-${SIMNIBS_VERSION}/freesurfer" >> ~/.bashrc && \
    echo "source \$FREESURFER_HOME/SetUpFreeSurfer.sh" >> ~/.bashrc

# Make sure scripts are executable
RUN chmod +x starter.sh main.sh sphere-analysis.sh gm_extract.py

# Copy project files into the container
COPY . .

# Set the entrypoint to the starter script
CMD ["./starter.sh"]

