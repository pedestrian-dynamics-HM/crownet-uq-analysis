import os

from utils.read_write_results import read_data, write_sobol_indices_to_file
import pandas as pd

if __name__ == "__main__":

    results_dir = os.path.join( os.path.dirname(os.getcwd()), "forward_propagation_2" )

    tikz_table = pd.DataFrame()

    for obs in [False, True]:
        for traf in [False, True]:

            results = os.path.join(
                results_dir, f"output_obstacle_{obs}_traf_{traf}"
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

    tikz_table.to_csv("results/DataTikzSubResults.dat", sep=" ")







