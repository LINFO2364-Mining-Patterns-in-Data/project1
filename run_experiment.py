import sys
import time
import csv
import os
import multiprocessing
import numpy as np
from tqdm import tqdm
from frequent_itemset_miner import apriori_no_pruning, apriori_pruning, alternative_miner


ALGORITHMS = ["alternative_miner", "apriori_pruning", "apriori_no_pruning"]
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]
RESULTS_DIR = "results_experiment"
TIMEOUT_LIMIT = 1000


def setup_results_file(dataset):
    filename = f"{RESULTS_DIR}/{dataset}.csv"
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["run", "algorithm", "threshold", "time"])
    return filename


def save_results(filename, run, algorithm, threshold, elapsed_time):
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([run, algorithm, threshold, round(elapsed_time, 6)])


def algorithm_wrapper(target_func, args, queue):
    """
    Wrapper function to run the algorithm and measure time.
    It puts the elapsed time in the queue.
    """
    start_time = time.time()
    target_func(*args)
    queue.put(time.time() - start_time)

def run_algorithm_with_timeout(target_func, args, timeout):
    """
    Runs the given function with a timeout. If it exceeds `timeout` seconds, 
    the process is terminated and `NaN` is returned.
    """
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=algorithm_wrapper, args=(target_func, args, queue))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        return np.nan
    return queue.get() if not queue.empty() else np.nan


def run_experiments(dataset, num_runs=1):
    results_file = setup_results_file(dataset)

    for threshold in THRESHOLDS:
        for algorithm in tqdm(ALGORITHMS, desc=f"Running experiment for `{threshold}` on `{dataset}`"):
            for run in range(1, num_runs + 1):
                algorithm_func = None

                if algorithm == "apriori_no_pruning":
                    algorithm_func = apriori_no_pruning
                elif algorithm == "apriori_pruning":
                    algorithm_func = apriori_pruning
                elif algorithm == "alternative_miner":
                    algorithm_func = alternative_miner

                if algorithm_func is not None:
                    elapsed_time = run_algorithm_with_timeout(
                        algorithm_func, 
                        (f"Datasets/{dataset}/{dataset}.dat", threshold, False, True), 
                        TIMEOUT_LIMIT
                    )
                    save_results(results_file, run, algorithm, threshold, elapsed_time)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python run_experiments.py <dataset_name> <num_runs(optional, default=1)>")
        sys.exit(1)

    if len(sys.argv) == 2:
        run_experiments(sys.argv[1])
    else:
        run_experiments(sys.argv[1], int(sys.argv[2]))
