import pandas as pd
import matplotlib.pyplot as plt
import sys

# Access the command-line arguments
if len(sys.argv) < 2:
    print("Please provide the report name!")
    sys.exit()

param = sys.argv[1]
report_path = f"results/{param}.csv"
print(f"Report path: {report_path}")

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

headers = ["Number of users", "AVG Response Time (seconds)"]

df = pd.read_csv(report_path)

plt.figure(figsize=(10, 6))  # Set the figure size
plt.plot(
    df["Number of users"],
    df["Response Time (seconds)"],
    marker="o",
    linestyle="-",
    color="b",
)

# Step 3: Customize the plot (optional)
plt.title(f"Results from '{report_path}'")  # Title
plt.xlabel("Number of Users")  # X-axis label
plt.ylabel("Response Time (seconds)")  # Y-axis label
plt.grid(True)

# Step 4: Display the plot
plt.show()
