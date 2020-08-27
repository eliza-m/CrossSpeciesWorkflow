#!/usr/bin/env bash

#should be run from project's folder

cd $CSW_HOME

#docker build -t quay.io/comp-bio-aging/species_proteins:latest -f dockerfiles/species_proteins/Dockerfile .

docker build -t quay.io/dbsb-ibar/species_proteins:latest -f dockerfiles/species_proteins/Dockerfile .