import csv
import os
import matplotlib.pyplot as plt

from dns_simulator import run_experiment


os.makedirs("results", exist_ok=True)


# ============================================================
# 1. TTL EXPERIMENT
# ============================================================

ttl_values = [5, 10, 20, 30, 60, 120, 300]

ttl_results = []

for ttl in ttl_values:
    result = run_experiment(
        mode="recursive",
        ttl=ttl,
        queries=2000,
        query_interval=1.0
    )

    ttl_results.append(result)


# Latency vs TTL
plt.figure(figsize=(8, 5))

plt.plot(
    ttl_values,
    [r["average_latency"] for r in ttl_results],
    marker="o"
)

plt.xlabel("TTL (seconds)")
plt.ylabel("Average Latency (ms)")
plt.title("DNS Average Latency vs TTL")
plt.grid(True)

plt.savefig(
    "results/latency_vs_ttl.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# Cache hit ratio vs TTL
plt.figure(figsize=(8, 5))

plt.plot(
    ttl_values,
    [r["cache_hit_ratio"] * 100 for r in ttl_results],
    marker="o"
)

plt.xlabel("TTL (seconds)")
plt.ylabel("Cache Hit Ratio (%)")
plt.title("DNS Cache Hit Ratio vs TTL")
plt.grid(True)

plt.savefig(
    "results/cache_hit_vs_ttl.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 2. RECURSIVE VS ITERATIVE
# ============================================================

recursive = run_experiment(
    mode="recursive",
    ttl=30,
    queries=2000,
    query_interval=1.0
)

iterative = run_experiment(
    mode="iterative",
    ttl=30,
    queries=2000,
    query_interval=1.0
)


methods = ["Recursive", "Iterative"]

average_latency = [
    recursive["average_latency"],
    iterative["average_latency"]
]

p95_latency = [
    recursive["p95_latency"],
    iterative["p95_latency"]
]


plt.figure(figsize=(8, 5))

x = range(len(methods))

plt.bar(
    x,
    average_latency,
    width=0.5
)

plt.xticks(x, methods)
plt.ylabel("Average Latency (ms)")
plt.title("Recursive vs Iterative DNS Resolution")
plt.grid(axis="y")

plt.savefig(
    "results/recursive_vs_iterative.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 3. SAVE CSV RESULTS
# ============================================================

with open(
    "results/results.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Mode",
        "TTL",
        "Average Latency (ms)",
        "P95 Latency (ms)",
        "Cache Hit Ratio (%)",
        "Cache Hits",
        "Total Queries"
    ])

    for r in ttl_results:
        writer.writerow([
            r["mode"],
            r["ttl"],
            round(r["average_latency"], 3),
            round(r["p95_latency"], 3),
            round(r["cache_hit_ratio"] * 100, 3),
            r["cache_hits"],
            r["total_queries"]
        ])

    writer.writerow([])

    writer.writerow([
        "recursive",
        30,
        round(recursive["average_latency"], 3),
        round(recursive["p95_latency"], 3),
        round(recursive["cache_hit_ratio"] * 100, 3),
        recursive["cache_hits"],
        recursive["total_queries"]
    ])

    writer.writerow([
        "iterative",
        30,
        round(iterative["average_latency"], 3),
        round(iterative["p95_latency"], 3),
        round(iterative["cache_hit_ratio"] * 100, 3),
        iterative["cache_hits"],
        iterative["total_queries"]
    ])


# ============================================================
# 4. PRINT SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DNS SIMULATION EXPERIMENT RESULTS")
print("=" * 60)

print("\nTTL Experiment:")

for r in ttl_results:
    print(
        f"TTL={r['ttl']:>3} s | "
        f"Latency={r['average_latency']:>6.2f} ms | "
        f"Cache Hit={r['cache_hit_ratio'] * 100:>6.2f}%"
    )

print("\nRecursive vs Iterative (TTL = 30s):")

print(
    f"Recursive : "
    f"{recursive['average_latency']:.2f} ms average, "
    f"{recursive['p95_latency']:.2f} ms P95"
)

print(
    f"Iterative : "
    f"{iterative['average_latency']:.2f} ms average, "
    f"{iterative['p95_latency']:.2f} ms P95"
)

print("\nFiles generated:")

print("  results/latency_vs_ttl.png")
print("  results/cache_hit_vs_ttl.png")
print("  results/recursive_vs_iterative.png")
print("  results/results.csv")

print("\nExperiment completed successfully.")