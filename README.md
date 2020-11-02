# Code for MDPI Entropy contribution

This repository contains the code for the article "Analysis of information dissemination through ad-hoc networks in a moving crowd" to be published in the Special Issue "Statistical Physics and Social Sciences" in Entropy published by MDPI.

## Init and update submodules
Init the submodules if necessary
Use
```
git submodule init
git submodule submodule --recursive
cd rover-main
git submodule init
git submodule submodule --recursive
cd ..
```
To produce the results presented in the MDPI article, use

```
./checkout_mdpi_state
```
## Set up the simulation model

Use
```
./install_rover
./pull_images.sh
```
to install the simulation model.

## Run the simulations
We use the python package suq-controller to run the simulations and to collect the results.
Install the virtual Python environment
```
cd uq
./install_venv
```
Activate the virtual environment
```
source .venv/bin/activate
```
Start the forward propagation
```
python3 forward_propagation_1/forward_propagation.py
```
## Analyse the results