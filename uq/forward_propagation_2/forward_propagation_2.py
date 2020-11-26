#!/usr/bin/env python3
#!/usr/bin/python3

import sys
from suqc import *

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))

from forward_propagation_1.forward_propagation import get_sampling_df
from utils.imports import path2ini, qoi
###############################################################################################################

from utils.read_write_results import read_data

def get_sampling(
    nr_samples=250, seed=111, is_test=False, obstacle_model=True, traffic=True
):

    param_values = get_sampling_df(nr_samples=nr_samples)

    if is_test:
        param_values["number_of_agents_mean"] = 30
        param_values = param_values.iloc[np.linspace(0,4),:]

    par_var = list()

    # Step 2.3: Create dictionary from dataframe which can be read by the suqc
    for x in range(len(param_values)):
        r = param_values.iloc[x].values

        dd = {
            "*.hostMobile[*].app[1].messageLength": r[5],
            "**wlan[*].radio.transmitter.power": r[6],
        }

        if obstacle_model is True:
            dd["*.radioMedium.obstacleLoss.typename"] = '"IdealObstacleLoss"'
        else:
            dd["*.radioMedium.obstacleLoss.typename"] = '""'

        if traffic is False:
            dd["*.hostMobile[*].app[1].startTime"] = "250s"

        d = {
            "dummy": {"number_of_agents_mean": r[0]},
            "vadere": {
                "sources.[id==1].distributionParameters": r[1],
                "sources.[id==2].distributionParameters": r[2],
                "sources.[id==5].distributionParameters": r[3],
                "sources.[id==6].distributionParameters": r[4],
                "attributesSimulation.fixedSeed": 65722447231342458,
            },
            "omnet": dd,
        }

        par_var.append(d)

    if nr_samples != len(par_var):
        print(
            f"WARNING: The number of required sampled is {nr_samples}. {len(par_var)} were produced."
        )

    return par_var


if __name__ == "__main__":

    #print(os.environ["ROVER_MAIN"])

    results = os.path.join(
        os.path.dirname(os.getcwd()), "forward_propagation_1/output_df"
    )
    __, dissemination_time = read_data(results, enable_plotting=False, remove_failed=False)

    sim_runs_larger_30s = (
        dissemination_time[dissemination_time["timeToInform95PercentAgents"] > 30]
        .index.get_level_values(0)
        .to_numpy()
    )

    for obs in [False, True]:
        for traf in [False, True]:

            par_var = get_sampling(
                nr_samples=2000, is_test=False, obstacle_model=obs, traffic=traf
            )

            # use simulations only with a dissemination time > 30s
            par_var = [par_var[x] for x in sim_runs_larger_30s]
            output_folder = os.path.join(
                os.getcwd(), f"output_obstacle_{obs}_traf_{traf}"
            )

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
                output_path=os.getcwd(),
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
            summary = output_folder + "_df"
            if os.path.exists(summary):
                shutil.rmtree(summary)

            os.makedirs(summary)

            env_man_info = setup.get_env_man_info()
            env_man_info.to_csv(os.path.join(summary, "envinfo.csv"))

            simulations = setup.get_simulations()
            simulations.to_csv(os.path.join(summary, "simulations.csv"))

            par_var, data = setup.run(15)

            par_var.to_csv(os.path.join(summary, "metainfo.csv"))

            data["poisson_parameter.txt"].to_csv(
                os.path.join(summary, "poisson_parameter.csv")
            )
            data["degree_informed_extract.txt"].to_csv(
                os.path.join(summary, "degree_informed_extract.csv")
            )
            data["time_95_informed.txt"].to_csv(
                os.path.join(summary, "time_95_informed.csv")
            )
            print(f"All simulation runs completed for {output_folder}.")
