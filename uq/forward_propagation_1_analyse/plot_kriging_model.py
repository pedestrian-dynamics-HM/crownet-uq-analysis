import pickle, os
from forward_propagation_1_analyse.sensitivity_analysis_stochastic import kriging
from utils.read_write_results import read_data
import numpy
import matplotlib.pyplot as plt

if __name__ == "__main__":
    results = os.path.join(
        os.path.dirname(os.getcwd()), "forward_propagation_1/output_df"
    )
    parameter, qoi = read_data(results, enable_plotting=False)

    var_name = "krigingResults.pickle"
    try:
        qoi_surr = pickle.load(open(var_name, "rb"))
    except (OSError, IOError) as e:
        # sobol indices for surrogate system
        qoi_surr, ssd = kriging(
            parameter,
            qoi,
            ints=numpy.arange(2000),
            exact_vals=False,
            enable_plotting=True,
            write_statistics=True,
        )
        pickle.dump(qoi_surr, open(var_name, "wb"))

    p1 = parameter["number_of_agents_mean"].values
    p2 = parameter["**wlan[*].radio.transmitter.power"].values
    p3 = parameter["*.hostMobile[*].app[1].messageLength"].values

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(p1, p2, qoi_surr, c=p3)
    ax.scatter(p1, p2, qoi, c="black")
    plt.show()

    plt.scatter(p1, qoi, c="black" )
    plt.scatter(p1, qoi_surr)
    plt.yscale("log")
    plt.show()

    parameter["real"] = qoi
    parameter["surrogate"] = qoi_surr

    parameter.columns = [
        "numberOfAgents",
        "Power",
        "Traffic",
        "Real",
        "Kriging"]

    parameter.to_csv("results/KrigingResults.dat", sep=" ", float_format='%.3f' )


    parameter['p1Group'] = parameter['numberOfAgents'].round(-3)
    parameter['p2Group'] = (parameter['Power']-0.25).round(0)
    parameter['p3Group'] = (parameter['Traffic']/2).round(-3)



    gb = parameter.groupby(by=["p1Group","p2Group"])

    groups = [gb.get_group(x) for x in gb.groups]

    for group in groups:
        p1 = group["numberOfAgents"].values
        p2 = group["Power"].values
        p3 = group["Traffic"].values
        qoi = group["Real"]
        qoi_surr = group["Kriging"]

        plt.scatter(p1, qoi, c="black")
        plt.scatter(p1, qoi_surr)
        plt.yscale("log")
        plt.ylim( (0,100))
        plt.title(f"power: {p2.min()} .. {p2.max()}, traffic: {p3.min()} .. {p3.max()}")
        plt.show()