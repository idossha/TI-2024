
# Stage 1: Start with the FreeSurfer image to extract necessary files
FROM freesurfer/freesurfer:7.1.1 AS freesurfer_stage

# Stage 2: Start with the FSL base image
FROM diannepat/fsl6

# Install necessary packages including Neovim, tmux, and GUI dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    bzip2 \
    build-essential \
    gcc \
    g++ \
    python3 \
    python3-pip \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libqt5widgets5 \
    libqt5gui5 \
    libqt5core5a \
    libqt5svg5 \
    libqt5opengl5 \
    libssl1.1 \
    libreoffice \
    openssl \
    jq \
    bc \
    vim \
    unzip \
    libxt6 \
    neovim \
    tmux \
    tcsh \
    tree \
    libglu1-mesa \
    mesa-utils \
    libgl1-mesa-dri \
    locales \
    fontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set locale and font configuration
RUN locale-gen en_US.UTF-8 \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && fc-cache -fv

# Set environment variables for Fontconfig and GUI applications
ENV FONTCONFIG_PATH=/etc/fonts
ENV XDG_RUNTIME_DIR=/tmp/runtime-root

# Ensure the XDG_RUNTIME_DIR is created with the right permissions
RUN mkdir -p /tmp/runtime-root && chmod 700 /tmp/runtime-root

# Copy FreeSurfer files from the first stage
COPY --from=freesurfer_stage /usr/local/freesurfer /usr/local/freesurfer

# Set environment variables for FreeSurfer
ENV FREESURFER_HOME=/usr/local/freesurfer
ENV SUBJECTS_DIR=$FREESURFER_HOME/subjects
ENV FS_LICENSE=$FREESURFER_HOME/license.txt
ENV PATH=$FREESURFER_HOME/bin:$PATH

# Copy the FreeSurfer license file into the container
COPY license.txt $FREESURFER_HOME/license.txt

# Download and install SimNIBS
RUN mkdir -p /simnibs && chmod -R 777 /simnibs
RUN wget https://github.com/simnibs/simnibs/releases/download/v4.1.0/simnibs_installer_linux.tar.gz -P /simnibs \
    && tar -xzf /simnibs/simnibs_installer_linux.tar.gz -C /simnibs
RUN /simnibs/simnibs_installer/install -s

# Set environment variables for SimNIBS
ENV PATH="/opt/simnibs-4.1/bin:$PATH"
ENV SIMNIBSDIR="/opt/simnibs-4.1"

# Set MATLAB Runtime version and installation directory
ENV MATLAB_RUNTIME_INSTALL_DIR=/usr/local/MATLAB/MATLAB_Runtime

# Download and install MATLAB Runtime R2024a
RUN wget https://ssd.mathworks.com/supportfiles/downloads/R2024a/Release/1/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2024a_Update_1_glnxa64.zip -P /tmp \
    && unzip -q /tmp/MATLAB_Runtime_R2024a_Update_1_glnxa64.zip -d /tmp/matlab_runtime_installer \
    && /tmp/matlab_runtime_installer/install -destinationFolder ${MATLAB_RUNTIME_INSTALL_DIR} -agreeToLicense yes -mode silent \
    && rm -rf /tmp/MATLAB_Runtime_R2024a_Update_1_glnxa64.zip /tmp/matlab_runtime_installer

# Set environment variables for MATLAB Runtime
ENV LD_LIBRARY_PATH="${MATLAB_RUNTIME_INSTALL_DIR}/v951/runtime/glnxa64:${MATLAB_RUNTIME_INSTALL_DIR}/v951/bin/glnxa64:${MATLAB_RUNTIME_INSTALL_DIR}/v951/sys/os/glnxa64:$LD_LIBRARY_PATH"
ENV XAPPLRESDIR=${MATLAB_RUNTIME_INSTALL_DIR}/v951/X11/app-defaults

# Clone the TI-CSC repository
RUN git clone https://github.com/idossha/new_TI-CSC.git /ti-csc

# Set the working directory to TI-CSC
WORKDIR /ti-csc

# Install Python dependencies
RUN pip3 install numpy scipy pandas

# Clone the Neovim configuration files repository
RUN git clone https://github.com/idossha/docker-congif-files.git /root/.config

# Install TPM (Tmux Plugin Manager)
RUN git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Move the .tmux.conf to the correct location
RUN mv /root/.config/.tmux.conf /root/.tmux.conf

# Source the .tmux.conf to apply the settings
RUN tmux source-file /root/.tmux.conf || true

# Entry point script to ensure XDG_RUNTIME_DIR exists
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Run the entrypoint script before starting bash
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
