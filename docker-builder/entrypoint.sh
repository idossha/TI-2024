#!/bin/bash
# Ensure XDG_RUNTIME_DIR is created with the right permissions
export XDG_RUNTIME_DIR=/tmp/runtime-root
mkdir -p $XDG_RUNTIME_DIR
chmod 700 $XDG_RUNTIME_DIR

# Run any other commands passed to the container
exec "$@"
