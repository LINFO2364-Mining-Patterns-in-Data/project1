import sys
import time
import csv
import os
import multiprocessing
import numpy as np
import psutil
from tqdm import tqdm
from frequent_itemset_miner import apriori_no_pruning, apriori_pruning, eclat

ALGORITHMS = ["eclat", "apriori_pruning", "apriori_no_pruning"]
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.05, 0.01, 0.005, 0.001]
# THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
# THRESHOLDS = [0.5, 0.1, 0.05, 0.01, 0.005, 0.001]
RESULTS_DIR = "results_experiment"
TIMEOUT_LIMIT = 1000

def setup_results_file(dataset):
    filename = f"{RESULTS_DIR}/{dataset}.csv"
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["run", "algorithm", "threshold", "time", "max_memory"])
    return filename

def save_results(filename, run, algorithm, threshold, elapsed_time, max_memory):
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([run, algorithm, threshold, round(elapsed_time, 6), round(max_memory, 2)])

def algorithm_wrapper(target_func, args, queue):
    """
    Wrapper function to run the algorithm, measure time, and track memory usage.
    It puts the elapsed time and max memory usage in the queue.
    """
    process = psutil.Process(os.getpid())  # Get current process
    mem_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB

    start_time = time.time()
    target_func(*args)
    elapsed_time = time.time() - start_time

    mem_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    max_memory = max(mem_before, mem_after)

    queue.put((elapsed_time, max_memory))

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
        return np.nan, np.nan

    return queue.get() if not queue.empty() else (np.nan, np.nan)

def run_experiments(dataset, num_runs=5):
    results_file = setup_results_file(dataset)
    has_timeout_already = [False, False, False]

    for threshold in THRESHOLDS:
        for algorithm in tqdm(ALGORITHMS, desc=f"Running experiment for `{threshold}` on `{dataset}`"):
            for run in range(1, num_runs + 1):
                algorithm_func = None

                if algorithm == "apriori_no_pruning" and not has_timeout_already[2]:
                    algorithm_func = apriori_no_pruning
                elif algorithm == "apriori_pruning" and not has_timeout_already[1]:
                    algorithm_func = apriori_pruning
                elif algorithm == "eclat" and not has_timeout_already[0]:
                    algorithm_func = eclat

                if algorithm_func is not None:
                    elapsed_time, max_memory = run_algorithm_with_timeout(
                        algorithm_func, 
                        (f"Datasets/{dataset}/{dataset}.dat", threshold, False, True), 
                        TIMEOUT_LIMIT
                    )
                    save_results(results_file, run, algorithm, threshold, elapsed_time, max_memory)
                    if np.isnan(elapsed_time):
                        has_timeout_already[ALGORITHMS.index(algorithm)] = True
                else:
                    save_results(results_file, run, algorithm, threshold, np.nan, np.nan)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python run_experiments.py <dataset_name> <num_runs(optional, default=1)>")
        sys.exit(1)

    if len(sys.argv) == 2:
        run_experiments(sys.argv[1])
    else:
        run_experiments(sys.argv[1], int(sys.argv[2]))
