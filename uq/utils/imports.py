import os


def problem_definition():
	problem = {
		"num_vars": 3,
		"names": [
			"number_of_agents_mean",
			"*.hostMobile[*].app[1].messageLength",
			"**wlan[*].radio.transmitter.power",
		],
		"bounds": [[0, 1], [0, 5000], [0.5, 2.0]],  # uniform distribution assumed!
	}
	return problem

def calc_second_order():
	return True

def get_seed():
	return 111

def path2ini():
	## Define the simulation to be used
	# A rover simulation is defined by an "omnetpp.ini" file and its corresponding directory.
	# Use following *.ini file:
	path2ini = os.path.join(
		os.environ["ROVER_MAIN"],
		"rover/simulations/simple_detoure_suqc_traffic/omnetpp.ini",
	)
	return path2ini

def qoi():
	## Define the quantities of interest (simulation output variables)
	# Make sure that corresponding post processing methods exist in the run_script2.py file
	qoi = [
		"degree_informed_extract.txt",
		"poisson_parameter.txt",
		"time_95_informed.txt",
	]
	return qoi

