import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


RESULTS_DIR = "results_experiment/"
PLOTS_DIR = "plots/"
DATASETS = {"accidents", "chess", "connect", "mushroom", "pumsb", "retail"}
ALGORITHMS = {"apriori_no_pruning", "apriori_pruning", "eclat"}
ALGORITHMS_NAMES = {
        "apriori_no_pruning": "Naive Apriori",
        "apriori_pruning": "Apriori Pruning",
        "eclat": "Eclat"
    }


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
            x=i,
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
    plt.savefig(os.path.join(PLOTS_DIR, f"{algorithm_name}_runtime_comparison.png"), dpi=300)
    plt.close()


def load_dataset_results(dataset_name):
    df = pd.read_csv(os.path.join(RESULTS_DIR, dataset_name + ".csv"))
    df = df.dropna()
    return df

def plot_dataset_runtime(df, dataset_name):
    """
    Plots the runtime of algorithms over different thresholds for a dataset.
    """
    import matplotlib.ticker as mticker
    df["threshold_pct"] = df["threshold"] * 100

    agg_df = df.groupby(["threshold_pct", "algorithm"]).agg(
        mean_time=("time", "mean"),
        std_time=("time", "std")
    ).reset_index()
    min_x = agg_df["threshold_pct"].min()
    max_x = agg_df["threshold_pct"].max()

    plt.figure(figsize=(7, 4))
    sns.set_style("white")
    sns.set_palette("grey")  # Force grayscale

    sns.lineplot(
        data=agg_df,
        x="threshold_pct",
        y="mean_time",
        hue="algorithm",
        style="algorithm",
        markers=True,       # Different markers to distinguish lines
        dashes=True,        # Use different dashes instead of colors
        linewidth=1.2,
        err_style="bars",
        errorbar=("sd")
    )

    plt.yscale("log")
    plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:.0f}"))
    # plt.xscale("log")

    plt.xlabel("Minimum Support (%)", fontsize=16)
    plt.ylabel("CPU Runtime (s)", fontsize=16)
    # plt.title(f"Database: {dataset_name}", fontsize=14)

    legend = plt.legend(loc="upper left", frameon=False)
    plt.setp(legend.get_texts(), fontsize=16)
    # plt.setp(legend.get_title(), fontsize=14)

    plt.grid(False)
    plt.xlim(min_x, max_x)
    plt.gca().invert_xaxis()
    plt.tight_layout()

    plt.savefig(f"{PLOTS_DIR}/{dataset_name}_runtime.png", dpi=300)
    plt.close()


def plot_dataset_memory(df, dataset_name):
    """
    Plots the runtime of algorithms over different thresholds for a dataset.
    """
    import matplotlib.ticker as mticker
    df["threshold_pct"] = df["threshold"] * 100

    agg_df = df.groupby(["threshold_pct", "algorithm"]).agg(
        mean_memory=("max_memory", "mean"),
        std_memory=("max_memory", "std")
    ).reset_index()
    min_x = agg_df["threshold_pct"].min()
    max_x = agg_df["threshold_pct"].max()

    plt.figure(figsize=(7, 4))
    sns.set_style("white")
    sns.set_palette("grey")  # Force grayscale

    sns.lineplot(
        data=agg_df,
        x="threshold_pct",
        y="mean_memory",
        hue="algorithm",
        style="algorithm",
        markers=True,       # Different markers to distinguish lines
        dashes=True,        # Use different dashes instead of colors
        linewidth=1.2,
        err_style="bars",
        errorbar=("sd")
    )

    plt.yscale("log")
    plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:.0f}"))
    # plt.xscale("log")

    plt.xlabel("Minimum Support (%)", fontsize=16)
    plt.ylabel("Main Memory (MB)", fontsize=16)
    # plt.title(f"Database: {dataset_name}", fontsize=14)

    legend = plt.legend(loc="upper left", frameon=False)
    plt.setp(legend.get_texts(), fontsize=16)
    # plt.setp(legend.get_title(), fontsize=14)

    plt.grid(False)
    plt.xlim(min_x, max_x)
    plt.gca().invert_xaxis()
    plt.tight_layout()

    plt.savefig(f"{PLOTS_DIR}/{dataset_name}_memory.png", dpi=300)
    plt.close()


# def plot_dataset_memory(df, dataset_name):
#     """
#     Plots a bar plot of max memory usage per algorithm, grouped by threshold using catplot.
#     """
#     df["threshold_pct"] = df["threshold"] * 100
    
#     agg_df = df.groupby(["threshold_pct", "algorithm"]).agg(
#         mean_memory=("max_memory", "mean")
#     ).reset_index()
    
#     algorithm_order = ["apriori_no_pruning", "apriori_pruning", "eclat"]
    
#     # Map algorithm names
#     agg_df["algorithm"] = agg_df["algorithm"].map(ALGORITHMS_NAMES)
    
#     # Adjust order based on display names
#     display_algorithm_order = [ALGORITHMS_NAMES[alg] for alg in algorithm_order]
#     agg_df["algorithm"] = pd.Categorical(agg_df["algorithm"], categories=display_algorithm_order, ordered=True)
    
#     agg_df = agg_df.sort_values(by=["threshold_pct", "algorithm"], ascending=[False, True])
    
#     sns.set_style("whitegrid")
    
#     g = sns.catplot(
#         data=agg_df,
#         x="algorithm",
#         y="mean_memory",
#         hue="algorithm",
#         hue_order=display_algorithm_order,
#         kind="bar",
#         col="threshold_pct",
#         col_wrap=2,
#         height=3,
#         aspect=1.2,
#         legend=False
#     )
    
#     g.set_axis_labels("", "Max Memory Usage (MB)")
#     g.set_titles("Minimum support: {col_name} (%)")
#     g.set(yscale="linear")
#     g.tight_layout()
    
#     plt.savefig(f"{PLOTS_DIR}/{dataset_name}_memory.png", dpi=300)
#     plt.close()


def plot_dataset_results(dataset_name):
    """
    Plots the impact of algorithms and threshold over the dataset.
    """
    df = load_dataset_results(dataset_name)
    plot_dataset_runtime(df, dataset_name)
    plot_dataset_memory(df, dataset_name)


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
    print("Plotting results of experiment...")
    
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    os.makedirs(PLOTS_DIR, exist_ok=True)
    process_files_in_folder()
