

def problem_definition():
	problem = {
		"num_vars": 3,
		"names": [
			"number_of_agents_mean",
			"*.hostMobile[*].app[1].messageLength",
			"**wlan[*].radio.transmitter.power",
		],
		"bounds": [[0, 1], [50, 5000], [0.5, 2.0]],  # uniform distribution assumed!
	}
	return problem

def calc_second_order():
	return True

def get_seed():
	return 111