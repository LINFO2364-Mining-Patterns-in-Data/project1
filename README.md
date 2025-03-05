## UCLouvain LINFO2364 - Mining Patterns in Data

This report presents an analysis and comparison of frequent item-set mining algorithms, focusing on the *Apriori* and *ECLAT* approaches. We implemented three variants: *Apriori Naive*, *Apriori Pruning*, and *ECLAT*, and evaluated their per- formance across multiple datasets with varying densities. The experiments assess computational efficiency in terms of execution time and memory consumption under different minimum support thresholds. Our findings highlight the strengths and weaknesses of each algorithm, demonstrating that *ECLAT* generally outperforms *Apriori* in dense datasets, while *Apriori Pruning* offers significant improvements over its naive counterpart.

## Project structure
- all implementations are within `frequent_itemset_miner.py`;
- generate solutions via `generate_resolutions.py`;
- checking if algorithms output the right result can be done through `smart_checker.py`;
- `run_experiment.py` allows to compute values over datasets with different minimum support threshold values;
- `plot_results.py` output graphs to compare results across dataset over runtime and memory metrics.
