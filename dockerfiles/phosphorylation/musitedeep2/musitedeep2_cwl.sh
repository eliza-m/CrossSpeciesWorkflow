#!/bin/bash

# workaround for CWL


mkdir -p $HOME/.keras/
cp /home/.keras/keras.json $HOME/.keras/keras.json

cd /home/MusiteDeep/MusiteDeep_Keras2.0/MusiteDeep/



# According to their documentation "prediction_batch.py" is main prediction file, however it has some errors when predicting Y residues. 
# However, "predict.py" works fine with tyrosines, but does not support kinase-specific.
# Therefore, we opted for the following workaround.

if [[ $6 == "general" ]]
then 
	python predict.py $1 $2 $3 $4 $5 $6 $7 $8;
else
	python predict_batch.py $1 $2 $3 $4 $5 $6 $7 $8;
fi

cp *.txt $HOME/





