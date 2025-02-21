import sys
import re
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

def get_patterns_from_file(filename):
    patterns = set()
    has_errors = False
    with open(filename) as f:
        for line in f:
            if line != "":
                g = re.search("\[((?:\d+,? ?)+)\] *(\(\d.\d+\))", line.rstrip())
                if g is None:
                    has_errors = True
                    print(f"[ERROR] The following line, from file {filename}, has the wrong format:")
                    print(f"\t{line}")
                else:
                    itemset = tuple(sorted([int(x) for x in g.group(1).split(', ')]))
                    patterns.add(itemset)
    return patterns if not has_errors else None
    
def compare_solution_files(expected_file, actual_file):
    """Compare the output of the patterns in actual with the patterns in expected"""
    expected_patterns = get_patterns_from_file(expected_file)
    actual_patterns = get_patterns_from_file(actual_file)
    if expected_patterns is not None and actual_patterns is not None:
        missed = expected_patterns - actual_patterns
        excess = actual_patterns - expected_patterns
        if len(missed) == 0 and len(excess) == 0:
            print("The files contain the same patterns")
        else:
            if len(missed) != 0:
                print("You missed some itemsets from the expected files:")
                to_show = list(missed)[:10] if len(missed) > 10 else list(missed)
                for pattern in to_show:
                    print(f"\t{pattern}")
                print(f"(Showed {len(to_show)} out of {len(missed)})")
            if len(excess) != 0:
                print("You returned unfrequent itemset:")
                to_show = list(excess)[:10] if len(excess) > 10 else list(excess)
                for pattern in to_show:
                    print(f"\t{pattern}")
                print(f"(Showed {len(to_show)} out of {len(excess)})")

def run_comparisons(dataset_name, algorithm):
    if dataset_name == "all":
        for name, runs in tqdm(DATASETS.items(), desc=f"Checking {algorithm} on {name} dataset"):
            for _, min_freq in runs:
                compare_solution_files(f"solutions/sols/{name}_{min_freq}", f"solutions/{algorithm}/{name}_{min_freq}")
    elif dataset_name in DATASETS:
        for _, min_freq in DATASETS[dataset_name]:
            compare_solution_files(f"solutions/sols/{dataset_name}_{min_freq}", f"solutions/{algorithm}/{dataset_name}_{min_freq}")
    else:
        print(f"Error: Unknown dataset '{dataset_name}'.")
        print("Available datasets:", ", ".join(DATASETS.keys()) + ", all")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python checker_smart.py <dataset_name> <algorithm>")
        sys.exit(1)

    run_comparisons(sys.argv[1], sys.argv[2])
