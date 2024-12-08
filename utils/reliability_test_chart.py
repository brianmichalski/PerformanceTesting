import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Access the command-line arguments
if len(sys.argv) < 2:
    print("Please provide the report name!")
    sys.exit()

report_file = sys.argv[1]
report_path = f"results/reliability/{report_file}.csv"
if not os.path.exists(report_path):
    print(f"File '{report_path}' doesn't exist!")
    sys.exit()

print(f"Report path: {report_path}")

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

headers = [
    "Elapsed time",
    "Response time",
    "Number of users",
    "Error rate",
    "Elapsed time (global)",
]

df = pd.read_csv(report_path)

# Plot the Response Time
sc = plt.scatter(
    df["Elapsed time"],
    df["Response time"],
    label="Response time",
    color="red",
    marker="o",
)

# Add the horizontal threshold line
threshold = 1.26
ax1 = plt.gca()  # Get the primary axes
ax1.axhline(y=threshold, color='green', linestyle='-', linewidth=2, label='Threshold (1.26)')

breakpoint_x = 230.051484
breakpoint_y = 1.26731133460998

# Add a vertical line at the first exceeding point
ax1.axvline(x=breakpoint_x, color='blue', linestyle='--', linewidth=2, label='Breakpoint (230.05)')

# Highlight the point on the chart
ax1.scatter(breakpoint_x, breakpoint_y, color='blue', zorder=5)

# Add titles, labels, and grid
ax1.set_title(f"Results from '{report_path}'")
ax1.set_xlabel("Test Elapsed Time (seconds)")
ax1.set_ylabel("Response time (seconds)")
ax1.grid(True)

# Add a secondary y-axis for Error Rate
ax2 = ax1.twinx()
line2, = ax2.plot(df["Elapsed time"], df["Error rate"], label="Error rate", color="purple", linestyle="--")
ax2.set_ylabel("Error Rate (%)")

# Combine the legends from both axes (primary and secondary axes)
handles, labels = ax1.get_legend_handles_labels()  
handles2, labels2 = ax2.get_legend_handles_labels() 

# Append the secondary axis handles and labels to the primary ones
handles.extend(handles2)
labels.extend(labels2)

# Show the combined legend
ax1.legend(handles, labels, loc='upper left')

plt.show()
