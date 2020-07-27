#!/bin/bash

# workaround for CWL

cd /home/DeepSumo

python3 predict_main.py --t1 $1 --t2 $2 -i $3 -o /home/

cat /home/result_output.txt > /${HOME}/output.txt









