import json
import matplotlib.pyplot as plt
import os


# Create output directory for the plots
os.makedirs("../../experiments/plots", exist_ok=True)


# filenames = ["sat_results_50_gsat", "sat_results_50_gsat-walk", "sat_results_50_wsat", "sat_results_50_schoening"]
filenames = ["sat_results_50_dpll", "sat_results_50_dpll-cdcl", "sat_results_50_ms", "sat_results_50_ms-ab"]


for filename in filenames:

    # Load the SAT results
    with open(f'../../experiments/{filename}.json', 'r') as f:
        sat_results = json.load(f)

    # Plotting
    for gamma, data in sat_results.items():
        ns = sorted(map(int, data.keys()))
        avg_iterations = []

        plt.figure(figsize=(10, 6))

        for n in ns:
            iterations = data[str(n)]  # json keys are strings
            if iterations:
                avg = sum(iterations) / len(iterations)
            else:
                avg = 0
            avg_iterations.append(avg)

            # Scatter individual points
            plt.scatter([n] * len(iterations), iterations, alpha=0.5)  # label=f"n={n}" if n == ns[0] else ""

        # Plot average line
        plt.plot(ns, avg_iterations, color='black', marker='o', label='Average')

        plt.title(f"SAT Solver Iterations for γ = {gamma} (= m / n)")
        plt.xlabel("n (number of variables)")
        plt.ylabel("Number of iterations")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Save each plot
        plt.savefig(f"../../experiments/plots/{filename}_gamma_{gamma}.png")
        plt.close()

    print("Plots saved in 'plots/' directory.")



