
import sys
from suqc import *



sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))

# This is just to make sure that the systems path is set up correctly, to have correct imports, it can be ignored:
from utils.imports import path2ini, qoi
from forward_propagation_1.forward_propagation import get_sampling


if __name__ == "__main__":

    ## Define which parameters are varied and store it in par_var
    par_var = get_sampling()
    par_var = [par_var(x) for x in [169,188,1552]]

    folder = os.path.abspath("../external_data/")
    output_folder = os.path.join(folder, "output_plots")

    model = CoupledConsoleWrapper(
        model="Coupled", vadere_tag="branch__shape_contains_loop_fix", omnetpp_tag="200221-1642"
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
        remove_output=False,
        seed_config={"vadere": "fixed", "omnet": "fixed"},
        env_remote=None,
    )

    if os.environ["ROVER_MAIN"] is None:
        raise SystemError(
            "Please add ROVER_MAIN to your system variables to run a rover simulation."
        )

    # Save results
    summary = os.path.join(os.getcwd(),"output_plots")
    if os.path.exists(summary):
        shutil.rmtree(summary)

    os.makedirs(summary)

    env_man_info = setup.get_env_man_info()
    env_man_info.to_csv(os.path.join(summary, "envinfo.csv"))

    simulations = setup.get_simulations()
    simulations.to_csv(os.path.join(summary, "simulations.csv"))

    par_var, data = setup.run(3)

    par_var.to_csv(os.path.join(summary, "metainfo.csv"))

    data["poisson_parameter.txt"].to_csv(os.path.join(summary, "poisson_parameter.csv"))
    data["degree_informed_extract.txt"].to_csv(
        os.path.join(summary, "degree_informed_extract.csv")
    )
    data["time_95_informed.txt"].to_csv(os.path.join(summary, "time_95_informed.csv"))

    print("All simulation runs completed.")