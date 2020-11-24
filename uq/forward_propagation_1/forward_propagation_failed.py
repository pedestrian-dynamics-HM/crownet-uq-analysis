#!/usr/bin/env python3
#!/usr/bin/python3

import sys
from suqc import *

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))

from forward_propagation_1.forward_propagation import get_sampling

# This is just to make sure that the systems path is set up correctly, to have correct imports, it can be ignored:
from utils.imports import problem_definition, get_seed, calc_second_order
from utils.imports import path2ini, qoi


run_local = True
###############################################################################################################

if __name__ == "__main__":

    ## Define which parameters are varied and store it in par_var
    par_var = get_sampling()
    failed_runs = [
        165,
        166,
        167,
        206,
        207,
        208,
        278,
        279,
        618,
        620,
        621,
        830,
        831,
        832,
        1153,
        1158,
        1159,
        1174,
        1387,
        1388,
        1527,
        1556,
        1557,
        1558,
        1559,
        1560,
        1896,
        1898,
        1899,
        1900,
        1901,
        1902,
        1904,
        1905,
        1907,
        1908,
        1909,
        1910,
        1911,
        1916,
        1917,
    ]
    par_var = [par_var[x] for x in failed_runs]
    folder = os.path.abspath("../external_data/")
    output_folder = os.path.join(folder, "output_failed")

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
    summary = os.path.join(os.getcwd(), "output_df_failed_reindex")
    if os.path.exists(summary):
        shutil.rmtree(summary)

    os.makedirs(summary)

    env_man_info = setup.get_env_man_info()
    env_man_info.to_csv(os.path.join(summary, "envinfo.csv"))

    simulations = setup.get_simulations()
    simulations.to_csv(os.path.join(summary, "simulations.csv"))

    par_var, data = setup.run(15)

    par_var.to_csv(os.path.join(summary, "metainfo.csv"))

    data["poisson_parameter.txt"].to_csv(os.path.join(summary, "poisson_parameter.csv"))
    data["degree_informed_extract.txt"].to_csv(
        os.path.join(summary, "degree_informed_extract.csv")
    )
    data["time_95_informed.txt"].to_csv(os.path.join(summary, "time_95_informed.csv"))


    print("All simulation runs completed.")
