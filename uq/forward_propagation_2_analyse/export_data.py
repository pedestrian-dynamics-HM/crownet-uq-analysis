import os

from utils.read_write_results import read_data, write_sobol_indices_to_file
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

    results = os.path.join(
        os.path.dirname(os.getcwd()), "forward_propagation_1/output_df"
    )
    __, dissemination_time = read_data(results, enable_plotting=False)

    sim_runs_larger_30s = (
        dissemination_time[dissemination_time["timeToInform95PercentAgents"] > 30]
        .index.get_level_values(0)
        .to_numpy()
    )


    results_dir = os.path.join( os.path.dirname(os.getcwd()), "forward_propagation_2" )

    tikz_table = pd.DataFrame()

    for obs in [True, False]:
        for traf in [True, False]:

            results = os.path.join(
                results_dir, f"output_obstacle_{obs}_traf_{traf}_df"
            )

            parameter, dissemination_time = read_data(results, enable_plotting=True)

            tikz_table = pd.concat([tikz_table, dissemination_time], axis=1)

    tikz_table = pd.concat([parameter, tikz_table], axis=1)

    tikz_table.columns = [
        "numberOfAgents",
        "Power",
        "Traffic",
        "timeDefault",
        "timeNoTraffic",
        "timeNothing",
        "timeTraffic",
    ]



    plt.scatter(tikz_table["numberOfAgents"], tikz_table["timeDefault"])
    plt.show()

    plt.scatter(tikz_table["numberOfAgents"],tikz_table["timeNoTraffic"] )
    plt.show()
    plt.scatter(tikz_table["numberOfAgents"], tikz_table["timeNothing"])
    plt.show()

    plt.scatter(tikz_table["numberOfAgents"], tikz_table["timeTraffic"])
    plt.show()

    tikz_table.to_csv("results/DataTikzSubResults.dat", sep=" ")







