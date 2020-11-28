import os

from utils.read_write_results import read_data
import pandas as pd


if __name__ == "__main__":

    results = os.path.join( os.path.dirname(os.getcwd()), "forward_propagation_1/output_df")
    parameter, dissemination_time = read_data(results, enable_plotting=True, remove_failed = True )

    # save results to files that can be read by latex
    tikz_table = pd.concat([parameter, dissemination_time], axis=1)
    tikz_table.columns = ["numberOfAgents", "Power", "Traffic", "timeToInform"]
    tikz_table.to_csv("results/DataTikz.dat", sep=" ")

    # get statistics
    stats = dissemination_time.describe()
    mode = dissemination_time.mode()
    mode = mode.rename(index={0: 'mode'})

    stats = pd.concat([stats, mode])
    stats = stats.round(2)
    stats.to_csv("results/DisseminationTimeStatistics.dat", sep = " ", header=False)

    p1 = len(tikz_table[ tikz_table["timeToInform"] <= 10 ]) / len(tikz_table["timeToInform"])
    p2 = len(tikz_table[tikz_table["timeToInform"] <= 30]) / len(tikz_table["timeToInform"])

    f = open("results/ProbabilitiesFailure.dat", "w+")
    f.write("Forward propagation 1, results\n \n")
    f.write(f"Probabilility time <= 10 {p1} \n")
    f.write(f"Probabilility time <= 30 {p2} \n")
    f.close()

    print("Finished.")



