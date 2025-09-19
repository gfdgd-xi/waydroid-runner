#!/bin/bash
WORKDIR=${PWD}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${WORKDIR}
exec "${PWD}/aapt2" "$@"

