import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Access the command-line arguments
if len(sys.argv) < 2:
    print("Please provide the report name!")
    sys.exit()

test_type = "load"

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

# Add vertical lines
L1_start = 5
L1_end = 70
plt.axvline(x=L1_start, color="red", linestyle="--", linewidth=2, label="L1")
plt.text(((L1_end - L1_start) / 2), 0.3, "L1", color="orange")

plt.axvline(x=L1_end, color="orange", linestyle="--", linewidth=2)

# Add another horizontal line
l1_time_range_limit = 0.73
plt.axhline(y=l1_time_range_limit, color="purple", linestyle="--", linewidth=2, label=f"{l1_time_range_limit}")
plt.text(L1_end * 1.2, l1_time_range_limit - 0.05, f"L1 max response time ({l1_time_range_limit})", color="purple")

# Add threshold horizontal line
threshold = 1.26
plt.axhline(y=threshold, color="g", linestyle="--", linewidth=2, label=f"Threshold ({threshold})")
plt.text(L1_end * 1.2, threshold + 0.05, f"Threshold ({threshold})", color="green")

plt.show()
