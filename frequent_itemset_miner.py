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
    Reads transactions from a dataset file and counts them.

    :param filepath: Path to the transaction dataset file
    :return transactions (list[frozensets]): List of transactions, each represented as a frozenset of integer items
    :return count (int): The total number of transactions read.
    """
    transactions = []
    count = 0
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                transaction = frozenset(map(int, line.split()))
                transactions.append(transaction)
                count += 1
    return transactions, count


def get_count_items(transactions):
    """
    Counts occurrences of each item in the list of transactions.

    :param list[frozenset] transactions: List of transactions, each represented as a frozenset of items
    :return item_counts (dict): Dictionary mapping each item to its occurrence count
    """
    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1
    return item_counts


def extract_dataset_name(filepath):
    """
    Extracts the dataset name from a given file path.
    The dataset name is assumed to be the first directory after "Datasets/" in the file path.

    :param filepath: Path to the dataset file
    :return dataset_name (str): The extracted dataset name
    """
    return filepath.split("/")[1]


def manage_output(itemsets, variant_name, dataset_name, minFrequency, is_test):
    """
    Manages the output of a variant of the Apriori algorithm by either printing results or saving them to a file.

    This function sorts the frequent itemsets, then:
    - If `is_test` is False, it prints the results to the terminal.
    - If `is_test` is True, it saves the results to a file in the "solutions/variant_name" directory.

    :param set itemsets: List of tuples, each containing a frequent itemset and its support value
    :param str variant_name: Name of the Apriori algorithm's variant
    :param str dataset_name: Name of the dataset for file saving
    :param int minFrequency: Minimum frequency threshold used to generate frequent itemsets
    :param boolean is_test: Flag indicating whether to print output (False) or save to a file (True)
    """
    itemsets.sort(key=lambda x: (x[0]))

    if not is_test:
        for itemset, support in itemsets:
            print(f"{itemset} ({'1.0' if support == 1 else f'{support:.17g}'})")
    
    if is_test:
        import os
        output_dir = f"solutions/{variant_name}"
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, f"{dataset_name}_{minFrequency}"), "w") as f:
            for itemset, support in itemsets:
                f.write(f"{itemset} ({'1.0' if support == 1 else f'{support:.17g}'})\n")


def apriori_pruning(filepath, minFrequency, is_test=False):
    """
    Runs the apriori algorithm variant with pruning, on the specified file with the given minimum frequency.

    :param filepath: Path to the transaction dataset file
    :param int minFrequency: Minimum frequency threshold to determine frequent itemsets
    :param boolean is_test: Flag indicating whether this run is a test (default: False)
    """
    transactions, num_transactions = read_transactions(filepath)
    min_support = minFrequency * num_transactions

    F_i = {frozenset([item]) for item, count in get_count_items(transactions).items() if count >= min_support}

    all_frequent_itemsets = []
    i = 1
    while F_i:
        for itemset in F_i:
            support = sum(1 for transaction in transactions if itemset.issubset(transaction)) / num_transactions
            all_frequent_itemsets.append((sorted(map(int, itemset)), support))

        C_i = set()
        F_i_list = list(F_i)
        for j in range(len(F_i_list)):
            for k in range(j + 1, len(F_i_list)):
                candidate = F_i_list[j] | F_i_list[k]
                if len(candidate) == i + 1:
                    if all(frozenset(subset) in F_i for subset in itertools.combinations(candidate, i)):
                        C_i.add(candidate)

        candidate_counts = {c: 0 for c in C_i}
        for transaction in transactions:
            for candidate in C_i:
                if candidate.issubset(transaction):
                    candidate_counts[candidate] += 1

        F_i = {itemset for itemset, count in candidate_counts.items() if count >= min_support}
        i += 1
    manage_output(all_frequent_itemsets, "apriori_pruning", extract_dataset_name(filepath), minFrequency, is_test)


def apriori_no_pruning(filepath, minFrequency, is_test=False):
    """
    Runs the apriori algorithm variant without pruning, on the specified file with the given minimum frequency, without pruning.

    :param filepath: Path to the transaction dataset file
    :param int minFrequency: Minimum frequency threshold to determine frequent itemsets
    :param boolean is_test: Flag indicating whether this run is a test (default: False)
    """
    transactions, num_transactions = read_transactions(filepath)
    min_support = minFrequency * num_transactions

    F_i = {frozenset([item]) for item, count in get_count_items(transactions).items() if count >= min_support}

    all_frequent_itemsets = []
    i = 1
    while F_i:
        for itemset in F_i:
            support = sum(1 for transaction in transactions if itemset.issubset(transaction)) / num_transactions
            all_frequent_itemsets.append((sorted(map(int, itemset)), support))

        C_i = set()
        F_i_list = list(F_i)
        for j in range(len(F_i_list)):
            for k in range(j + 1, len(F_i_list)):
                candidate = F_i_list[j] | F_i_list[k]
                if len(candidate) == i + 1:
                    C_i.add(candidate)

        candidate_counts = {c: 0 for c in C_i}
        for transaction in transactions:
            for candidate in C_i:
                if candidate.issubset(transaction):
                    candidate_counts[candidate] += 1

        F_i = {itemset for itemset, count in candidate_counts.items() if count >= min_support}
        i += 1
    manage_output(all_frequent_itemsets, "apriori_no_pruning", extract_dataset_name(filepath), minFrequency, is_test)


def apriori(filepath, minFrequency, is_test=False):
    """
    Runs an apriori algorithm variant for Inginious, on the specified file with the given minimum frequency.

    :param filepath: Path to the transaction dataset file
    :param int minFrequency: Minimum frequency threshold to determine frequent itemsets
    :param boolean is_test: Flag indicating whether this run is a test (default: False)
    """
    apriori_pruning(filepath, minFrequency, is_test)


def eclat(prefix_tids, items, vertical_db, min_support, num_transactions, prefix=[]):
    """
    Recursive DFS/ECLAT function to find frequent itemsets.
    
    :param list[int] prefix_tids: Set of TIDs (transaction IDs) containing the current prefix
    :param list items: List of candidate items to extend the current prefix
    :param dict vertical_db: Vertical database mapping items to sets of TIDs
    :param int min_support: Minimum support count required to consider itemset frequent
    :param int num_transactions: Total number of transactions (used for frequency calculation)
    :param list[items] prefix: Current prefix itemset
    :return frequent_itemsets (list): List of frequent itemsets found along with their frequencies
    """
    all_frequent_itemsets = []

    for i in range(len(items)):
        item = items[i]
        new_tids = prefix_tids & vertical_db[item]

        if len(new_tids) >= min_support:
            new_prefix = prefix + [int(item)]
            frequency = len(new_tids) / num_transactions
            all_frequent_itemsets.append((sorted(new_prefix), frequency))

            new_items = items[i+1:]
            new_vertical_db = {}

            for next_item in new_items:
                intersected = vertical_db[next_item] & new_tids
                if len(intersected) >= min_support:
                    new_vertical_db[next_item] = intersected

            deeper_frequent_itemsets = eclat(new_tids, list(new_vertical_db.keys()), new_vertical_db,
                                             min_support, num_transactions, prefix=new_prefix)
            all_frequent_itemsets.extend(deeper_frequent_itemsets)
    return all_frequent_itemsets


def create_vertical_db(transactions):
    """
    Builds a vertical database from a list of transactions.

    :param list[frozenset] transactions: List of transactions, each represented as a frozenset of integer items
    :return vertical_db (dict): Vertical database mapping items to sets of TIDs (transaction IDs)
    """
    vertical_db = {}
    for tid, transaction in enumerate(transactions):
        for item in transaction:
            if item not in vertical_db:
                vertical_db[item] = set()
            vertical_db[item].add(tid)
    return vertical_db


def alternative_miner(filepath, minFrequency, is_test=False):
    """
    Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency (DFS/ECLAT).
    
    :param filepath: Path to the transaction dataset file
    :param int minFrequency: Minimum frequency threshold to determine frequent itemsets
    :param boolean is_test: Flag indicating whether this run is a test (default: False)
    """
    transactions, num_transactions = read_transactions(filepath)
    min_support = minFrequency * num_transactions

    vertical_db = create_vertical_db(transactions)

    all_items = sorted(vertical_db.keys(), key=lambda x: int(x))

    prefix_tids = set(range(num_transactions))
    all_frequent_itemsets = eclat(prefix_tids, all_items, vertical_db, min_support, num_transactions)

    manage_output(all_frequent_itemsets, "alternative_miner", extract_dataset_name(filepath), minFrequency, is_test)
