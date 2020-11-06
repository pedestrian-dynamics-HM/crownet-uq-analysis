import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def write_sobol_indices_to_file(Si1, filename):

    with open(filename, "w") as f:

        f.write(
            "The following data was produced by SALib.analyze.sobol.analyze (rounded to 3 digits) \n\n"
        )

        f.write("If the data is a vector: \n")
        f.write("Element 1 corresponds to the parameter: number_of_agents_mean\n"),
        f.write("Element 2 corresponds to the parameter: Traffic\n"),
        f.write("Element 3 corresponds to the parameter: Power,\n"),

        f.write(
            "If the data is a matrix, interaction between the elements are described. \n"
        )
        f.write("In this case, use the reference from above. \n\n\n")

        for k, v in Si1.items():
            f.write(str(k) + " >>> " + str(np.round(v, 3)) + "\n\n")
        f.write("95-Confidence Intervals of S1, S2 and ST \n")
        f.write("LB: Lower Bound, UB: Upper bound\n\n")
        for si in ["S1", "S2", "ST"]:
            f.write(
                f"{si}CI95LB"
                + " >>> "
                + str(np.round(Si1[f"{si}"] - Si1[f"{si}_conf"], 3))
                + "\n\n"
            )
            f.write(
                f"{si}CI95UB"
                + " >>> "
                + str(np.round(Si1[f"{si}"] + Si1[f"{si}_conf"], 3))
                + "\n\n"
            )
    print(f"Saved Sobol indices to {filename}")


def write_regr_coefs_to_file(regression_coef, filename):

    with open(filename, "w") as f:
        f.write(
            "The following data contains the regression coefficients of the surrogate models. \n\n"
        )
        f.write(str(np.round(regression_coef, 3)) + "\n")
        f.write(str(np.round(regression_coef, 3)) + "\n")


def get_succesful_simulation_runs(parameter, degree):
    # check the results

    # check return code
    len_demanded = len(parameter)
    parameter = parameter[parameter["('MetaInfo', 'return_code')"] == 0]
    indices_1 = parameter.index.get_level_values(0)

    # check data
    degree = degree[~degree.index.duplicated(keep="last")]
    degree = degree[degree.iloc[:, 0] >= 0.95]
    indices_2 = degree.index.get_level_values(0)

    indices_successful_sim_runs = indices_1.intersection(indices_2)
    l = len(indices_successful_sim_runs)

    # provide indices of succesful simulation runs
    # make sure that the number is a multiple of 8 as required by SALib settings
    indices_failed_sim_runs = indices_1.difference(
        indices_successful_sim_runs
    )



    if len(indices_failed_sim_runs) > 0:
        print(
            f"WARNING: \t {len_demanded} samples were demanded.  {len(indices_failed_sim_runs)} simulation runs failed."
        )
        print(f"\t\t\t Failed: {indices_failed_sim_runs.to_list()}.")

    return indices_successful_sim_runs.to_numpy(), indices_failed_sim_runs.to_numpy()


def read_data(summary, enable_plotting=False, remove_failed = True):

    # Check data
    parameter = pd.read_csv(
        os.path.join(summary, "metainfo.csv"), index_col=["id", "run_id"]
    )

    degree = pd.read_csv(
        os.path.join(summary, "degree_informed_extract.csv"), index_col=[0, 1]
    )
    degree = degree[["percentageInformed-PID12"]]

    # check results and remove failed simulation runs from database
    succeeded, failed = get_succesful_simulation_runs(parameter, degree)


    # extract data, remove units
    parameter = parameter.iloc[:, 0:3]
    parameter.columns = [c_name.split("'")[5] for c_name in parameter.columns.to_list()]
    print("Extracted parameters:")
    for col in parameter.columns.to_list():
        print(f"\tParameter: {col}")
        try:
            parameter[col] = (
                parameter[col].str.extract(r"(\d+(\.\d+)?)").astype("float")
            )
        except:
            pass

    dissemination_time = pd.read_csv(
        os.path.join(summary, "time_95_informed.csv"), index_col=[0, 1]
    )
    dissemination_time = dissemination_time[["timeToInform95PercentAgents"]]
    dissemination_time = dissemination_time.sort_index()

    # remove failed simulation runs

    dissemination_time_r = dissemination_time.iloc[succeeded, :]
    parameter_r = parameter.iloc[succeeded, :]

    if remove_failed == True:
        dissemination_time = dissemination_time_r
        parameter = parameter_r
        print(f"Removed failed simulations {list(failed)} from database.")
    else:
        average_val = dissemination_time_r.mean().to_numpy().ravel()[0]
        dissemination_time.iloc[failed, :] = average_val
        print(f"WARNING Assigned average dissemination time value of succesful simulatioon runs ({average_val:4.2f}) to failed simulations runs {list(failed)}.")


    if enable_plotting:
        p1 = parameter["number_of_agents_mean"].values
        p2 = parameter["**wlan[*].radio.transmitter.power"].values
        p3 = parameter["*.hostMobile[*].app[1].messageLength"].values

        plt.hist(dissemination_time.to_numpy(), bins=50, density=True, alpha=0.5)
        plt.xlabel("Time [s] to inform 95% of agents")
        plt.ylabel("Probability density function")
        plt.show(block=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(p1, p2, p3)
        plt.show(block=False)

        for p in [p1, p2, p3]:
            plt.hist(p, bins=6)
            plt.show(block=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        ax.scatter(p1, p2, p3, c=dissemination_time.values)
        plt.show(block=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        ax.scatter(p1, p2, dissemination_time.values, c=p3)
        plt.show(block=False)

    return parameter, dissemination_time
