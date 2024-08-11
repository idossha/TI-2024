#!/bin/bash

# Allow local root access to X server
xhost +local:root

# Prompt the user to input the path to the local project directory
echo "Give path to local project dir:"
read LOCAL_PROJECT_DIR

# Extract the project directory name from the provided path
PROJECT_DIR_NAME=$(basename "$LOCAL_PROJECT_DIR")

# Run the Docker container with the specified settings
docker run --rm -ti \
  -e DISPLAY=$DISPLAY \
  -e LIBGL_ALWAYS_SOFTWARE=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "$LOCAL_PROJECT_DIR":/mnt/"$PROJECT_DIR_NAME" \
  ti-package:v.1.0.1

# Revert X server access permissions
xhost -local:root

