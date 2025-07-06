import json
import matplotlib.pyplot as plt
import os
import sys


# === Configuration ===
os.makedirs("../../experiments/plots", exist_ok=True)
# filenames = ["sat_results_50_gsat", "sat_results_50_gsat-walk", "sat_results_50_wsat"]  # , "sat_results_50_schoening"
filenames = ["sat_results_50_dpll", "sat_results_50_dpll-cdcl", "sat_results_50_ms", "sat_results_50_ms-ab"]


# === Plot Setup ===
plt.figure(figsize=(10, 6))

for filename in filenames:
    # Use file name (without directory and extension) as label
    # label = os.path.splitext(os.path.basename(filename))[0]

    with open(f'../../experiments/{filename}.json', 'r') as f:
        sat_results = json.load(f)

    # Assume all gammas are included, we plot one line per gamma
    for gamma, data in sat_results.items():
        ns = sorted(map(int, data.keys()))
        avg_iterations = []

        for n in ns:
            iterations = data[str(n)]
            avg = sum(iterations) / len(iterations) if iterations else 0
            avg_iterations.append(avg)

        plt.plot(ns, avg_iterations, marker='o', label=f"{filename}, γ={gamma}")

# === Finalize Plot ===
plt.title("Comparison of SAT Solver Averages Across Datasets")
plt.xlabel("n (Number of Variables)")
plt.ylabel("Average Iterations (Brute Force)")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig("comparison_plot.png")
# plt.show()
