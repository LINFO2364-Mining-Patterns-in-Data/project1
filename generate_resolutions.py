from frequent_itemset_miner import apriori
import sys
import time
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


def generate_res():
    if len(sys.argv) != 3:
        print("Usage: python generate_resolutions.py <dataset_name> <algorithm>")
        print("Example: python main.py toy apriori")
        print("Available datasets:", ", ".join(DATASETS.keys()) + ", all")
        sys.exit(1)

    dataset_name = sys.argv[1]
    algorithm = sys.argv[2]

    if dataset_name == "all":
        for name in DATASETS.keys():
            for filepath, min_freq in tqdm(DATASETS[name], desc=f"Running `{algorithm}` on `{name}` dataset"):
                if algorithm == "apriori":
                    apriori(filepath, min_freq, True)
    
    elif dataset_name in DATASETS:
        for filepath, min_freq in tqdm(DATASETS[dataset_name], desc=f"Running `{algorithm}` on `{dataset_name}` dataset"):
            if algorithm == "apriori":
                apriori(filepath, min_freq, True)
    
    else:
        print(f"Error: Unknown dataset '{dataset_name}'.")
        print("Available datasets:", ", ".join(DATASETS.keys()) + ", all")
        sys.exit(1)


if __name__ == "__main__":
    start_time = time.time()
    generate_res()
    end_time = time.time()
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
