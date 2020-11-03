import os

from SALib.analyze.sobol import analyze
from utils.imports import problem_definition, calc_second_order, get_seed
from utils.read_write_results import read_data, write_sobol_indices_to_file

def sobolanalysis(qoi, normalize=True, num_resamples=100):

    problem = problem_definition()

    Si = analyze(
        problem,
        qoi,
        calc_second_order=calc_second_order(),
        print_to_console=False,
        seed=get_seed(),
        num_resamples=num_resamples,
    )

    return Si


if __name__ == "__main__":

    plot_ = False
    normalize = False
    models = 100

    results = os.path.join(os.getcwd(), "output_df")
    parameter, qoi = read_data(results, enable_plotting=False)

    # sobol indices for real system
    Si = sobolanalysis(qoi.to_numpy(), num_resamples=100)
    write_sobol_indices_to_file(Si, filename="SobolIndicesRealSystem.dat")
