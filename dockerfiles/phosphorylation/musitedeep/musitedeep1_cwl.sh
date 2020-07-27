#!/bin/bash

# workaround for CWL


mkdir -p $HOME/.keras/
cp /home/.keras/keras.json $HOME/.keras/keras.json

cd /home/MusiteDeep/MusiteDeep/
python predict.py $1 $2 $3 $4 $5 $6 $7 $8

cp *.txt $HOME/





