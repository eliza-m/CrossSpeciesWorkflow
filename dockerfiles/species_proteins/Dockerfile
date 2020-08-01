FROM quay.io/comp-bio-aging/base:latest


COPY species_proteins/ /opt/species_proteins/
COPY environment.yaml /opt/species_proteins/
WORKDIR /opt/species_proteins

RUN conda env create -f environment.yaml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "species_proteins", "/bin/bash", "-c"]

# Make sure the environment is activated:
RUN echo "environment is installed!"
RUN python -c "from bioservices import *"

# The code to run when container is started:
ENTRYPOINT ["conda", "run", "-n", "species_proteins", "python", "workflow/run.py"]