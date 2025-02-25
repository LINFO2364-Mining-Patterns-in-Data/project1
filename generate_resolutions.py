from frequent_itemset_miner import apriori_no_pruning, apriori_pruning, alternative_miner
import sys
import time
import csv
import os
from tqdm import tqdm

DATASETS = {
    "toy": [
        ("Datasets/toy/toy.dat", 0.125),
        ("Datasets/toy/toy.dat", 0.4),
        ("Datasets/toy/toy.dat", 0.25),
    ],
    "accidents": [
        ("Datasets/accidents/accidents.dat", 0.8),
        ("Datasets/accidents/accidents.dat", 0.9),
        ("Datasets/accidents/accidents.dat", 0.85),
    ],
    "chess": [
        ("Datasets/chess/chess.dat", 0.7),
        ("Datasets/chess/chess.dat", 0.8),
        ("Datasets/chess/chess.dat", 0.9),
    ],
    "connect": [
        ("Datasets/connect/connect.dat", 0.95),
        ("Datasets/connect/connect.dat", 0.97),
        ("Datasets/connect/connect.dat", 0.98),
    ],
    "mushroom": [
        ("Datasets/mushroom/mushroom.dat", 0.3),
        ("Datasets/mushroom/mushroom.dat", 0.5),
        ("Datasets/mushroom/mushroom.dat", 0.8),
    ],
    "pumsb": [
        ("Datasets/pumsb/pumsb.dat", 0.9),
        ("Datasets/pumsb/pumsb.dat", 0.95),
        ("Datasets/pumsb/pumsb.dat", 0.97),
    ],
    "retail": [
        ("Datasets/retail/retail.dat", 0.1),
        ("Datasets/retail/retail.dat", 0.02),
        ("Datasets/retail/retail.dat", 0.05),
    ],
}


def setup_results_file(algorithm):
    """
    Ensures that the results CSV file is created from scratch for each new execution.
    If the file exists, it is deleted and recreated with the correct headers.

    :param str algorithm: Name of the algorithm variant
    """
    filename = f"results_experiment/{algorithm}.csv"
    os.makedirs("results_experiment", exist_ok=True)

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["run", "dataset", "threshold", "time"])


def save_results(algorithm, run, dataset, threshold, elapsed_time):
    """
    Saves the experiment results (run number, dataset, threshold, elapsed time) into a CSV file.
    The CSV file is stored at results_experiment/{algorithm}.csv.

    :param str algorithm: Name of the algorithm variant
    :param int run: Run number
    :param str dataset: Name of the dataset
    :param int threshold: Minimum frequency threshold
    :param float elapsed_time: Execution time in seconds
    """
    filename = f"results_experiment/{algorithm}.csv"

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([run, dataset, threshold, round(elapsed_time, 6)])


def generate_res(dataset_name, algorithm, num_runs):
    """
    Runs the specified algorithm on the given dataset(s) multiple times, measuring execution time and saving results.
    
    :param str dataset_name: Name of the dataset to run the algorithm on
    :param str algorithm: Name of the algorithm variant
    :param int num_runs: Number of times the algorithm is run
    """
    setup_results_file(algorithm)
    
    for i in range(int(num_runs)):
        if dataset_name == "all":
            for name in tqdm([key for key in DATASETS.keys() if key != "toy"], desc= f"Run [{i+1}/{num_runs}] for `{algorithm}` on all datasets"):
                for filepath, min_freq in DATASETS[name]:
                    
                    start_time = time.time()
                    
                    if algorithm == "apriori_no_pruning":
                        apriori_no_pruning(filepath, min_freq, False, False)
                    elif algorithm == "apriori_pruning":
                        apriori_pruning(filepath, min_freq, False, False)
                    elif algorithm == "alternative_miner":
                        alternative_miner(filepath, min_freq, False, False)
                    else:
                        print(f"Error: Unknown algorithm '{algorithm}'.")
                        print("Available algorithms: apriori_no_pruning, apriori_pruning, alternative_miner")
                        sys.exit(1)
                    
                    save_results(algorithm, i+1, name, min_freq, time.time() - start_time)
        
        elif dataset_name in DATASETS:
            for filepath, min_freq in tqdm(DATASETS[dataset_name], desc=f"Run [{i+1}/{num_runs}] for `{algorithm}` on `{dataset_name}` dataset"):

                start_time = time.time()

                if algorithm == "apriori_no_pruning":
                    apriori_no_pruning(filepath, min_freq, False, False)
                elif algorithm == "apriori_pruning":
                    apriori_pruning(filepath, min_freq, False, False)
                elif algorithm == "alternative_miner":
                    alternative_miner(filepath, min_freq, False, False)
                else:
                    print(f"Error: Unknown algorithm '{algorithm}'.")
                    print("Available algorithms: apriori_no_pruning, apriori_pruning, alternative_miner")
                    sys.exit(1)

                save_results(algorithm, i+1, name, min_freq, time.time() - start_time)
        
        else:
            print(f"Error: Unknown dataset '{dataset_name}'.")
            print("Available datasets:", ", ".join(DATASETS.keys()) + ", all")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_resolutions.py <dataset_name> <algorithm> <num_runs>\n")
        print("Note: toy is not run if <dataset_name> is set to 'all'.")
        print("Warning: using a high value for <num_runs> may take a long time to complete.\n")
        print("Example: python generate_resolutions.py toy apriori 1\n")
        sys.exit(1)

    if sys.argv[3].isdigit() and int(sys.argv[3]) < 1:
        print("Error: Number of runs must be a positive integer.")
        sys.exit(1)
    
    generate_res(sys.argv[1], sys.argv[2], int(sys.argv[3]))
