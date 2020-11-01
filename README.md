# mdpi-rover-2020

## Init and update submodules
Use
```
cd rover-main
git submodule init
git submodule update --recursive
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
