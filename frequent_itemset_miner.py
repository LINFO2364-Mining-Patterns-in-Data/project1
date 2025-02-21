"""
Skeleton file for the project 1 of the LINGI2364 course.
Use this as your submission file. Every piece of code that is used in your program should be put inside this file.

This file given to you as a skeleton for your implementation of the Apriori and Depth
First Search algorithms. You are not obligated to use them and are free to write any class or method as long as the
following requirements are respected:

Your apriori and alternativeMiner methods must take as parameters a string corresponding to the path to a valid
dataset file and a double corresponding to the minimum frequency.
You must write on the standard output (use the print() method) all the itemsets that are frequent in the dataset file
according to the minimum frequency given. Each itemset has to be printed on one line following the format:
[<item 1>, <item 2>, ... <item k>] (<frequency>).

The items in an itemset must be printed in lexicographical order. However, the itemsets themselves can be printed in
any order.

Do not change the signature of the apriori and alternative_miner methods as they will be called by the test script.

__authors__ = Group23, Cyril Bousmar, Mohamed-Anass Gallass
"""

import itertools
import re

class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath):
        """reads the dataset file and initializes files"""
        self.transactions = list()
        self.items = set()

        try:
            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            for line in lines:
                transaction = list(map(int, line.split(" ")))
                self.transactions.append(transaction)
                for item in transaction:
                    self.items.add(item)
        except IOError as e:
            print("Unable to read dataset file!\n" + e)

    def trans_num(self):
        """Returns the number of transactions in the dataset"""
        return len(self.transactions)

    def items_num(self):
        """Returns the number of different items in the dataset"""
        return len(self.items)

    def get_transaction(self, i):
        """Returns the transaction at index i as an int array"""
        return self.transactions[i]
    
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


def read_transactions(filepath):
    """
    Reads transactions from a dataset file and counts item occurrences.
    Each line in the file represents a transaction, where items are space-separated. 
    The function parses these transactions and maintains a count of individual item occurrences.

    Parameters:
    -----------
    filepath : str
        The path to the transaction dataset file.

    Returns:
    --------
    tuple
        A tuple containing:
        - transactions (list of frozensets): A list where each transaction is stored as a frozenset of items.
        - item_counts (dict): A dictionary mapping each item to its occurrence count in the dataset.
    """
    transactions = []
    item_counts = {}

    with open(filepath, 'r') as file:
        for line in file:
            transaction = frozenset(line.strip().split())
            transactions.append(transaction)
            for item in transaction:
                item_counts[item] = item_counts.get(item, 0) + 1
    return transactions, item_counts


def extract_dataset_name(filepath):
    """
    Extracts the dataset name from a given file path.
    The dataset name is assumed to be the first directory after "Datasets/" in the file path.
    
    Parameters:
    -----------
    filepath : str
        The full path to the dataset file.

    Returns:
    --------
    str
        The extracted dataset name.
    """
    return filepath.split("/")[1]


def manage_output(all_frequent_itemsets, filepath, minFrequency, is_test):
    """
    Manages the output of the Apriori algorithm by either printing results or saving them to a file.

    This function sorts the frequent itemsets, then:
    - If `is_test` is False, it prints the results to the terminal.
    - If `is_test` is True, it saves the results to a file in the "solutions/apriori" directory.

    Parameters:
    -----------
    all_frequent_itemsets : list of tuples
        A list of tuples where each tuple contains a frequent itemset (as a sorted list) and its support value.
    filepath : str
        The path of the dataset file, used to extract the dataset name for file saving.
    minFrequency : float
        The minimum frequency threshold used to generate frequent itemsets.
    is_test : bool
        A flag that determines whether to print the output (False) or save it to a file for testing (True).
    """
    all_frequent_itemsets.sort(key=lambda x: (x[0]))

    if not is_test:
        for itemset, support in all_frequent_itemsets:
            print(f"{itemset} ({support:.3g})")
    
    if is_test:
        import os
        output_dir = "solutions/apriori"
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, f"{extract_dataset_name(filepath)}_{minFrequency}"), "w") as f:
            for itemset, support in all_frequent_itemsets:
                f.write(f"{itemset} ({support:.3g})\n")


def apriori(filepath, minFrequency, is_test=False):
    """
    Runs the apriori algorithm on the specified file with the given minimum frequency
    """
    transactions, item_counts = read_transactions(filepath)
    num_transactions = len(transactions)
    min_support = minFrequency * num_transactions

    # Create candidates itemset of size 1
    F_i = {frozenset([item]) for item, count in item_counts.items() if count >= min_support}

    all_frequent_itemsets = []
    i = 1
    while F_i:
        # Store sorted frequent itemsets of size i with proper support values for output
        for itemset in F_i:
            support = sum(1 for transaction in transactions if itemset.issubset(transaction)) / num_transactions
            all_frequent_itemsets.append((sorted(map(int, itemset)), support))

        # Generate candidates of size i + 1
        C_i = set()
        F_i_list = list(F_i)
        for j in range(len(F_i_list)):
            for k in range(j + 1, len(F_i_list)):
                candidate = F_i_list[j] | F_i_list[k]
                if len(candidate) == i + 1:

                    # Pruning infrequent candidates
                    if all(frozenset(subset) in F_i for subset in itertools.combinations(candidate, i)):
                        C_i.add(candidate)

        # Compute support for each candidate
        candidate_counts = {c: 0 for c in C_i}
        for transaction in transactions:
            for candidate in C_i:
                if candidate.issubset(transaction):
                    candidate_counts[candidate] += 1

        # Remove candidates that do not meet the minimum support
        F_i = {itemset for itemset, count in candidate_counts.items() if count >= min_support}
        i += 1

    manage_output(all_frequent_itemsets, filepath, minFrequency, is_test)


def alternative_miner(filepath, minFrequency):
    """Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency"""
    # TODO: either second implementation of the apriori algorithm or implementation of the depth first search algorithm
    print("Not implemented")
