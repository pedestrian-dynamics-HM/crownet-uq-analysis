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


def read_data(summary, enable_plotting=False):

    # Step 1: read and plot parameter

    parameter = pd.read_csv(
        os.path.join(summary, "metainfo.csv"), index_col=["id", "run_id"]
    )
    len_demanded = len(parameter)
    parameter = parameter[parameter["('MetaInfo', 'return_code')"] == 0]
    if len_demanded != len(parameter):
        print(
            f"WARNING: {len_demanded} samples were demanded. Resuls are available for {len(parameter)} samples."
        )

    # extract data:
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

    res = pd.read_csv(os.path.join(summary, "poisson_parameter.csv"), index_col=[0, 1])
    res = res[["PoissonParameter"]]
    res = res.sort_index()

    res2 = pd.read_csv(os.path.join(summary, "time_95_informed.csv"), index_col=[0, 1])
    res2 = res2[["timeToInform95PercentAgents"]]
    res2 = res2.sort_index()
    m_val = m_val = (
        res2.drop(index=[1424, 1426, 1427, 1428]).mean().values[0]
    )  # remove effect of failed simulations
    res2[res2["timeToInform95PercentAgents"] == 0] = m_val
    qoi = pd.concat([res, res2], axis=1)

    ############
    # plot data

    tikz_table = pd.concat([parameter, res2], axis=1)
    tikz_table.columns = ["numberOfAgents", "Power", "Traffic", "timeToInform"]
    tikz_table.to_csv("DataTikz.dat", sep=" ")

    if enable_plotting:
        p1 = parameter["number_of_agents_mean"].values
        p2 = parameter["**wlan[*].radio.transmitter.power"].values
        p3 = parameter["*.hostMobile[*].app[1].messageLength"].values

        plt.hist(res2.to_numpy(), bins=50, density=True, alpha=0.5)
        plt.xlabel("Time [s] to inform 95% of agents")
        plt.ylabel("Probability density function")
        plt.legend(labels=["Before transformation", "After transformation"])
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

        ax.scatter(p1, p2, p3, c=res2.values)
        plt.show(block=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        ax.scatter(p1, p2, res2.values, c=p3)
        plt.show(block=False)

    return parameter, qoi["timeToInform95PercentAgents"]
