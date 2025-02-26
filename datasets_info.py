import os
import csv
from tqdm import tqdm

DATASETS = ["accidents", "chess", "connect", "mushroom", "pumsb", "retail"]
DATASETS_DIR = "Datasets"
OUTPUT_CSV = "datasets_summary.csv"

def process_dataset(filepath):
    """
    Reads a dataset file, counts unique items and transactions in a single pass.

    :param str filepath: Path to the dataset file
    :return Tuple: database name, unique item count, transaction count
    """
    unique_items = set()
    transaction_count = 0

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                transaction = set(map(int, line.split()))
                unique_items.update(transaction)
                transaction_count += 1

    database_name = os.path.basename(filepath)
    return database_name, len(unique_items), transaction_count

def process_all_datasets():
    """
    Processes all datasets in the DATASETS list and saves results in a CSV file.
    """
    results = []

    for dataset in tqdm(DATASETS, desc="Processing datasets"):
        dataset_path = os.path.join(f"{DATASETS_DIR}/{dataset}/", f"{dataset}.dat")
        db_name, num_items, num_transactions = process_dataset(dataset_path)
        results.append((db_name, num_items, num_transactions))


    with open(f"{DATASETS_DIR}/{OUTPUT_CSV}", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["database", "items", "transactions"])
        writer.writerows(results)

    print(f"Results saved to {DATASETS_DIR}/{OUTPUT_CSV}")

if __name__ == "__main__":
    process_all_datasets()