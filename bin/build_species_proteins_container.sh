#!/usr/bin/env bash

#should be run from project's folder
docker build -t quay.io/comp-bio-aging/species_proteins:latest -f dockerfiles/species_proteins/Dockerfile .