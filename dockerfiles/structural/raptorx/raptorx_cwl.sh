rm /home/TGT_Package/databases/uniprot20

ln -s $DBfolder /home/TGT_Package/databases/$DBname

cd /home/

TGT_Package/A3M_TGT_Gen.sh -i $1 -h $3 -d $2 -c $4 -m $5 -o /output/;

Predict_Property/Predict_Property.sh -i /output/*.tgt -o /output/

chmod -R 777 /output

cp -r /output/*.* ${HOME}/






