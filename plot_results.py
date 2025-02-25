import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


RESULTS_DIR = "results_experiment/"
PLOTS_DIR = "plots/"
DATASETS = {"toy", "accidents", "chess", "connect", "mushroom", "pumsb", "retail"}
ALGORITHMS = {"apriori_no_pruning", "apriori_pruning", "alternative_miner"}


def load_algorithm_results(algorithm_name):
    return pd.read_csv(os.path.join(RESULTS_DIR, algorithm_name + ".csv"))

def plot_algorithm_results(algorithm_name):
    df = load_algorithm_results(algorithm_name)

    df["dataset_threshold"] = df["dataset"] + " (T=" + df["threshold"].astype(str) + ")"

    agg_df = df.groupby(["dataset", "dataset_threshold"]).agg(
        mean_time=("time", "mean"),
        std_time=("time", "std")
    ).reset_index()

    plt.figure(figsize=(14, 7))
    sns.set_style("whitegrid")

    ax = sns.barplot(
        data=agg_df,
        x="dataset_threshold",
        y="mean_time",
        hue="dataset",
        capsize=0.1,
        errorbar=None
    )

    for i, row in agg_df.iterrows():
        plt.errorbar(
            x=i,  # x-position of the bar
            y=row["mean_time"],
            yerr=row["std_time"],
            fmt='none',
            capsize=5,
            color='black'
        )

    plt.xticks(rotation=45, ha="right")
    plt.xlabel("{Dataset, Threshold} Pairs")
    plt.ylabel("Mean Execution Time (s)")
    plt.title(f"Runtime Comparison Across Datasets for {algorithm_name}")
    plt.legend(title="Datasets", loc="upper right", frameon=True)
    plt.tight_layout()
    
    # Save plot
    plt.savefig(os.path.join(PLOTS_DIR, f"{algorithm_name}_runtime_comparison.png"), dpi=300)
    plt.close()


def load_dataset_results(dataset_name):
    df = pd.read_csv(os.path.join(RESULTS_DIR, dataset_name + ".csv"))
    df = df.dropna()
    return df

def plot_dataset_results(dataset_name):
    """
    Plots the impact of algorithms and threshold over the dataset.
    """
    df = load_dataset_results(dataset_name)

    df["threshold_pct"] = df["threshold"] * 100

    agg_df = df.groupby(["threshold_pct", "algorithm"]).agg(
        mean_time=("time", "mean"),
        std_time=("time", "std")
    ).reset_index()

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")

    sns.lineplot(
        data=agg_df,
        x="threshold_pct",
        y="mean_time",
        hue="algorithm",
        marker="o",
        linewidth=1
    )
    plt.yscale("log")
    plt.xlabel("Minimum Support (%)")
    plt.ylabel("Total Time (sec) (Log Scale)")
    plt.title("Algorithm Runtime Comparison on Different Minimum Support Thresholds")
    plt.legend(title="Algorithm", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(f"{dataset_name}_by_algorithms.png", dpi=300)


def process_files_in_folder():
    """
    Reads files in a folder and runs `plot_dataset` if the filename matches a dataset,
    or `plot_algorithm` if the filename matches an algorithm.
    """
    for filename in os.listdir(RESULTS_DIR):
        name, ext = os.path.splitext(filename)

        if ext != ".csv":
            continue
        elif name in DATASETS:
            plot_dataset_results(name)
        elif name in ALGORITHMS:
            plot_algorithm_results(name)


if __name__ == "__main__":
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    print("Plotting results of experiment...")
    os.makedirs(PLOTS_DIR, exist_ok=True)
    process_files_in_folder()
