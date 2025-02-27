import os
import csv
from tqdm import tqdm

DATASETS = ["accidents", "chess", "connect", "mushroom", "pumsb", "retail"]
DATASETS_DIR = "Datasets"
OUTPUT_CSV = "datasets_summary.csv"

def process_dataset(filepath):
    """
    Reads a dataset file, counts unique items, transactions, and estimates density.

    :param str filepath: Path to the dataset file
    :return Tuple: database name, unique item count, transaction count, density
    """
    unique_items = set()
    transaction_count = 0
    total_items_count = 0

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                transaction = set(map(int, line.split()))
                unique_items.update(transaction)
                transaction_count += 1
                total_items_count += len(transaction)

    database_name = os.path.splitext(os.path.basename(filepath))[0]
    
    num_items = len(unique_items)

    density = total_items_count / (transaction_count * num_items) if num_items > 0 else 0

    return database_name, num_items, transaction_count, density

def process_all_datasets():
    """
    Processes all datasets in the DATASETS list and saves results in a CSV file.
    """
    results = []

    for dataset in tqdm(DATASETS, desc="Processing datasets"):
        dataset_path = os.path.join(f"{DATASETS_DIR}/{dataset}/", f"{dataset}.dat")
        db_name, num_items, num_transactions, density = process_dataset(dataset_path)
        results.append((db_name, num_items, num_transactions, round(density, 4)))

    output_path = os.path.join(DATASETS_DIR, OUTPUT_CSV)
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["database", "items", "transactions", "density"])
        writer.writerows(results)

    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    process_all_datasets()
