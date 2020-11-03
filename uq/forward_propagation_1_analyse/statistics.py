import os

from utils.read_write_results import read_data, write_sobol_indices_to_file
import pandas as pd


if __name__ == "__main__":

    results = os.path.join( os.path.dirname(os.getcwd()), "forward_propagation_1/output_df")
    parameter, dissemination_time = read_data(results, enable_plotting=True)

    # get statistics
    stats = dissemination_time.describe()
    mode = dissemination_time.mode()
    mode = mode.rename(index={0: 'mode'})

    stats = pd.concat([stats, mode])
    stats = stats.round(2)
    stats.to_csv("results/DisseminationTimeStatistics.dat", sep = " ", header=False)

    print("Finished.")



