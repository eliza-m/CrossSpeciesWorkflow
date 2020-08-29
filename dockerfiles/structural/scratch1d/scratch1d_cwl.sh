#!/usr/bin/env bash


bash /home/SCRATCH-1D_1.2/bin/run_SCRATCH-1D_predictors.sh $1 /output/$2 $3

chmod -R 777 /output
cp /output/* ${HOME}/


