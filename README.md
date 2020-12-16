# Code for MDPI Entropy contribution

This repository contains the code for the article "Analysis of information dissemination through ad-hoc networks in a moving crowd" to be published in the Special Issue "Statistical Physics and Social Sciences" in Entropy published by MDPI.

## Contents of this repository
This repository contains 
* the source code of the **CrowNet** simulator that is included as git submodule.
* the source code and the result data that we use in the forward propgation and in the sensitivity analyses. 

### CrowNet

**CrowNet** is developed by the members of the research project *Improving the efficiency of traffic infrastructures by robust internetworking (roVer)* of the Hochschule Muenchen University of Applied Sciences.
See https://www.hm.edu/en/research/projects/project_details/wischhof_koester/rover.en.html for information about *roVer*.

*Currently, CrowNet is embedded as git-submodule rover-main*.
We plan to change the repository name from rover-main to CrowNet in 2021.

### Result data
The results data files are stored in ```uq/..``` next to the scripts that are used to generate the data.

### Scripts for uncertainty quantification
The scripts used for uncertainty can be found under ```uq/..```.


## System requirements (hardware)
A system with >=250GB RAM and >=80 cores is required, because the simulations take ~6 days.


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
If the simulation fails, restart the script.

## Analyse the results
After the simulation has finished, we analyse the results.
We compute the statistics of the resulting empirical distribution.

```
python3 forward_propagation_1_analyse/statistics.py

```
We analyse why information dissemination sometimes failes
```
python3 forward_propagation_2/forward_propagation_2.py
python3 forward_propagation_2_analyse/export_data.py

```

We use sensitivity analysis to quantify the influence of the parameters

```
python3 forward_propagation_1_analyse/sensitivity_analysis.py
```
We use a kriging model and repeat the sensitivity analysis
```
python3 forward_propagation_1_analyse/sensitivity_analysis_stochastic.py
```


