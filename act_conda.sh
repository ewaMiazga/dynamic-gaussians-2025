#!/bin/bash

__conda_setup="$('scratch/cvlab/home/miazga/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "scratch/cvlab/home/miazga/miniconda3/etc/profile.d/conda.sh" ]; then
        . "scratch/cvlab/home/miazga/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="scratch/cvlab/home/miazga/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup

eval "$(/scratch/cvlab/home/miazga/miniconda3/bin/conda shell.bash hook)"

export TORCH_HOME=/scratch/cvlab/home/miazga
export CUDA_HOME=/usr/local/cuda-12.4
export PATH=${CUDA_HOME}/bin:${PATH}
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:$LD_LIBRARY_PATH
