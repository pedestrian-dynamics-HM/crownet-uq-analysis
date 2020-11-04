import os

from SALib.analyze.sobol import analyze
from utils.imports import problem_definition, calc_second_order, get_seed
from utils.read_write_results import read_data, write_sobol_indices_to_file

def sobolanalysis(qoi):

    problem = problem_definition()

    Si = analyze(
        problem,
        qoi,
        calc_second_order=calc_second_order(),
        print_to_console=False,
        seed=get_seed(),
    )

    return Si


if __name__ == "__main__":

    results = os.path.join( os.path.dirname(os.getcwd()), "forward_propagation_1/output_df")
    parameter, dissemination_time = read_data(results, enable_plotting=True)
    # apply sensitivity analysis under the assumption that the system is deterministic
    Si = sobolanalysis(dissemination_time.to_numpy())
    write_sobol_indices_to_file(Si, filename="results/SobolIndicesRealSystem.dat")
