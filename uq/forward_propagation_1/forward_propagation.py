#!/usr/bin/env python3
#!/usr/bin/python3

import sys
from suqc import *

from SALib.sample import saltelli
import scipy.stats as sp

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))

# This is just to make sure that the systems path is set up correctly, to have correct imports, it can be ignored:
from utils.imports import problem_definition, get_seed, calc_second_order
from utils.imports import path2ini, qoi


run_local = True
###############################################################################################################

def get_sampling_df(nr_samples=2000):

    # the following 3 parameters are varied

    # 1) number_of_agents_mean:
    ## the number of agents generated in 100s
    ## lower bound: 10, upper bound: 2000
    ## distribution: truncated exponential

    # 2) *.hostMobile[*].app[1].messageLength
    ## is used to vary the network load, traffic load = messageLength*20ms
    ## lower bound: 50B, upper bound: 5000B (video streaming in medium quality)
    ## distribution: uniform

    # 3) **wlan[*].radio.transmitter.power
    ## is used to define the transmission power of the WLAN ad hoc network
    ## lower bound: 0.50mW, upper bound: 2.00mW
    ## distribution: uniform

    # STEP 1: Create samples with Sobol sequence using SALib

    parameter = problem_definition()

    param_values = saltelli.sample(
        parameter, int(nr_samples/8), calc_second_order=calc_second_order(), seed=get_seed()
    )
    # Step 1.1: Transform random variable 1)
    low = 10
    up = 2000
    b = 4
    param_values[:, 0] = sp.truncexpon.ppf(
        param_values[:, 0], b=b, loc=low, scale=(up - low) / b
    )

    # Step 2: Make samples readable for suqc
    param_values = pd.DataFrame(
        param_values, columns=["number_of_agents_mean", "p1", "p2"]
    )
    param_values["number_of_agents_mean"] = round(
        param_values["number_of_agents_mean"], 0
    )

    # Step 2.1: Distribute number of agents at four sources and determine number of agents/(1 second)
    for x in [1, 2, 5, 6]:
        param_values[f"sources.[id=={x}].distributionParameters"] = param_values.apply(
            lambda row: [row.number_of_agents_mean * 0.01 / 4], axis=1
        )

    # Step 2.2: Add units
    param_values["*.hostMobile[*].app[1].messageLength"] = param_values.apply(
        lambda row: f"{int(row.p1)}B", axis=1
    )
    param_values["**wlan[*].radio.transmitter.power"] = param_values.apply(
        lambda row: f"{round(row.p2,2)}mW", axis=1
    )
    param_values = param_values.drop(columns=["p1", "p2"])
    return param_values

def get_sampling(nr_samples=2000, is_test=False):

    param_values = get_sampling_df(nr_samples=nr_samples)

    if is_test:
        param_values["number_of_agents_mean"] = 30
        param_values = param_values.iloc[np.linspace(0,4),:]

    par_var = list()

    # Step 2.3: Create dictionary from dataframe which can be read by the suqc
    for x in range(len(param_values)):
        r = param_values.iloc[x].values
        d = {
            "dummy": {"number_of_agents_mean": r[0]},
            "vadere": {
                "sources.[id==1].distributionParameters": r[1],
                "sources.[id==2].distributionParameters": r[2],
                "sources.[id==5].distributionParameters": r[3],
                "sources.[id==6].distributionParameters": r[4],
            },
            "omnet": {
                "*.hostMobile[*].app[1].messageLength": r[5],
                "**wlan[*].radio.transmitter.power": r[6],
            },
        }
        par_var.append(d)

    if nr_samples != len(par_var):
        print(f"WARNING: The number of required sampled is {nr_samples}. {len(par_var)} were produced.")

    return par_var


if __name__ == "__main__":

    ## Define which parameters are varied and store it in par_var
    par_var = get_sampling()

    folder = os.path.abspath("../external_data/")
    output_folder = os.path.join(folder, "output")

    model = CoupledConsoleWrapper(
        model="Coupled", vadere_tag="200527-1424", omnetpp_tag="200221-1642"
    )

    setup = CoupledDictVariation(
        ini_path=path2ini(),
        config="final",
        parameter_dict_list=par_var,
        qoi=qoi(),
        model=model,
        scenario_runs=1,
        post_changes=PostScenarioChangesBase(apply_default=True),
        output_path=folder,
        output_folder=output_folder,
        remove_output=True,
        seed_config={"vadere": "fixed", "omnet": "fixed"},
        env_remote=None,
    )

    if os.environ["ROVER_MAIN"] is None:
        raise SystemError(
            "Please add ROVER_MAIN to your system variables to run a rover simulation."
        )

    # Save results
    summary = os.path.join(os.getcwd(),"output_df")
    if os.path.exists(summary):
        shutil.rmtree(summary)

    os.makedirs(summary)

    env_man_info = setup.get_env_man_info()
    env_man_info.to_csv(os.path.join(summary, "envinfo.csv"))

    simulations = setup.get_simulations()
    simulations.to_csv(os.path.join(summary, "simulations.csv"))

    par_var, data = setup.run(10)

    par_var.to_csv(os.path.join(summary, "metainfo.csv"))

    data["poisson_parameter.txt"].to_csv(os.path.join(summary, "poisson_parameter.csv"))
    data["degree_informed_extract.txt"].to_csv(
        os.path.join(summary, "degree_informed_extract.csv")
    )
    data["time_95_informed.txt"].to_csv(os.path.join(summary, "time_95_informed.csv"))

    print("All simulation runs completed.")
