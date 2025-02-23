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


def manage_output(itemsets, variant_name, dataset_name, minFrequency, is_test):
    """
    Manages the output of a variant of the Apriori algorithm by either printing results or saving them to a file.

    This function sorts the frequent itemsets, then:
    - If `is_test` is False, it prints the results to the terminal.
    - If `is_test` is True, it saves the results to a file in the "solutions/variant_name" directory.

    Parameters:
    -----------
    itemsets : list of tuples
        A list of tuples where each tuple contains a frequent itemset (as a sorted list) and its support value.
    variant_name : str
        The name of the Apriori algorithm's variant.
    dataset_name : str
        The dataset name for file saving.
    minFrequency : float
        The minimum frequency threshold used to generate frequent itemsets.
    is_test : bool
        A flag that determines whether to print the output (False) or save it to a file for testing (True).
    """
    itemsets.sort(key=lambda x: (x[0]))

    if not is_test:
        for itemset, support in itemsets:
            print(f"{itemset} ({support:.17g})")
    
    if is_test:
        import os
        output_dir = f"solutions/{variant_name}"
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, f"{dataset_name}_{minFrequency}"), "w") as f:
            for itemset, support in itemsets:
                #f.write(f"{itemset} ({support:.3g})\n") -> error pour les cas de checker (1) et pas (1.0S)
                f.write(f"{itemset} ({support:.15f})\n")
                


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

    manage_output(all_frequent_itemsets, "apriori", extract_dataset_name(filepath), minFrequency, is_test)



def alternative_miner(filepath, minFrequency, is_test=False):
    """
    Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency (DFS/ECLAT)
    """
    print(" - START", 10*"-")
    print(" - Filepath : ",filepath)
    # -------------------------------------------------------------------------
    # 1) Read the dataset
    print(" - STEP 1 : Read the db")
    transactions, _ = read_transactions(filepath)
    #print(transactions)
    num_transactions = len(transactions)
    min_support = minFrequency * num_transactions
    #print("min_support   : ",min_support)

    # -------------------------------------------------------------------------
    # 2) Build a vertical database: for each item, which transaction IDs (TIDs) contain it?
    vertical_db = {}
    for tid, transaction in enumerate(transactions):
        for item in transaction:
            if item not in vertical_db:
                vertical_db[item] = set()
            vertical_db[item].add(tid)

    print(" - STEP 2 : Build the vertical-db")
    #print(vertical_db)

    # Sort items so we generate itemsets
    all_items = sorted(vertical_db.keys(), key=lambda x: int(x))
    #print(" - All items : ",all_items)

    # A list to hold all frequent itemsets found
    all_frequent_itemsets = []

    # DFS function to find frequent itemsets
    def eclat(prefix, prefix_tids, items, vertical_db):
        # For each candidate item in 'items', try to extend the prefix
        for i in range(len(items)):
            item = items[i]
            # Intersect TIDs to find the new set of common transactions
            new_tids = prefix_tids & vertical_db[item]
            # Check if this new itemset is still frequent
            if len(new_tids) >= min_support:

                # Build the extended prefix
                new_prefix = prefix + [int(item)]

                # Store it in all_frequent_itemsets
                frequency = len(new_tids) / num_transactions
                all_frequent_itemsets.append((sorted(new_prefix), frequency))

                # Extend with items that come after the current one
                new_items = items[i+1:]


                # Build a smaller vertical DB for these new candidates
                new_vertical_db = {}
                for next_item in new_items:
                    # Intersect TIDs with new_tids
                    intersected = vertical_db[next_item] & new_tids
                    if len(intersected) >= min_support:
                        new_vertical_db[next_item] = intersected


                # Recurse
                #print(20*"-")
                #print("RECURSE ECLAT :")
                #print("new_prefix  :\n ",new_prefix)
                #print("new_tids  :\n", new_tids)
                #print("list(new_vertical_db.keys())  :\n",list(new_vertical_db.keys()))
                #print("new_vertical_db  : \n",new_vertical_db)
                #print(20*"-")
                eclat(new_prefix, new_tids, list(new_vertical_db.keys()), new_vertical_db)

    # -------------------------------------------------------------------------
    # 3) Call the DFS function starting from an empty prefix and all items
    #    prefix_tids is the set of all TIDs initially
    print(" - STEP 3 : Call the DFS function")

    prefix=[]
    prefix_tids=set(range(num_transactions)) 
    items=all_items
    vertical_db=vertical_db

    print(20*"-")
    print("ECLAT :")
    print("prefix  :\n ",prefix)
    print("prefix_tids  :\n", prefix_tids)
    print("items  :\n",items)
    print("vertical_db  : \n",vertical_db)
    print(20*"-")

    eclat(prefix=[],
          prefix_tids=set(range(num_transactions)), 
          items=all_items,
          vertical_db=vertical_db)

    # -------------------------------------------------------------------------
    # 4) Output
    print(" - STEP 4 : Generate output")
    #print("all_frequent_itemsets  :\n", all_frequent_itemsets)
    manage_output(all_frequent_itemsets, "alternative_miner", extract_dataset_name(filepath), minFrequency, is_test)
    print(" - DONE", 10*"-", "\n")
