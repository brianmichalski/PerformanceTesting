import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Access the command-line arguments
if len(sys.argv) < 2:
    print("Please provide the report name!")
    sys.exit()

test_type = "stress_load_balance"

report_file = sys.argv[1]
report_path = f"results/{test_type}/{report_file}.csv"
if not os.path.exists(report_path):
    print(f"File '{report_path}' doesn't exist!")
    sys.exit()

print(f"Report path: {report_path}")

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

headers = ["Number of users", "AVG Response Time", "Median Response Time"]

df = pd.read_csv(report_path)

# Plot the response time
plt.plot(
    df["Number of users"],
    df["AVG Response Time"],
    marker="o",
    linestyle="-",
    color="b",
)

# Title and labels
plt.title(f"Results from '{report_path}'")
plt.xlabel("Number of Users")
plt.ylabel("Response Time (avg)")
plt.grid(True)

# Add vertical lines (load ranges)
load_ranges = [
    ["L1", "red", 5, 73],
    ["L2", "orange", 119, 170],
    ["L3", "red", 247, 324],
    ["L4", "orange", 509, 649],
    ["L5", "red", 1000, 1250],
    ["L6", "orange", 2250, 2500],
]
for range in load_ranges:
    label = range[0]
    color = range[1]
    L_start = range[2]
    L_end = range[3]
    label_position = L_end - ((L_end - L_start) / 2) - 20
    plt.axvline(x=L_start, color=color, linestyle="--", linewidth=2, label=label)
    plt.axvline(x=L_end, color=color, linestyle="--", linewidth=2)
    plt.text(label_position, 0.3, label, color=color)

# Add another horizontal line
l1_time_range_limit = 0.73
plt.axhline(
    y=l1_time_range_limit,
    color="purple",
    linestyle="--",
    linewidth=2,
    label=f"{l1_time_range_limit}",
)
plt.text(
    670,
    l1_time_range_limit - 0.12,
    f"L1 max response time ({l1_time_range_limit})",
    color="purple",
)

# Add threshold horizontal line
threshold = 1.26
plt.axhline(
    y=threshold,
    color="g",
    linestyle="--",
    linewidth=2,
)
plt.text(670, threshold + 0.05, f"Threshold ({threshold})", color="green")

plt.show()
