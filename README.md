# Performance Testing for Online News Site

This document provides instructions for setting up and running performance tests on the **OnlineNewsSite** app as part of the Non-Functional Testing course (PROG8051). The testing includes **load**, **stress**, and **reliability** testing for both the Midterm and Final projects.

## App Under Test

The application being tested is an **Online News Site**. It allows users to browse news articles, search for topics, and interact with content. The app is hosted on GitHub: [OnlineNewsSite](https://github.com/MobinaJafarian/OnlineNewsSite).

You will need to clone the repository into both the `midterm` and `finalproject` (pending) directories within the Vagrant setup.

## Vagrant Setup

There are two Vagrant setups available:

- **Midterm Setup (`vagrant/midterm/Vagrantfile`)**: This setup contains two separate machines—one for the **web server** and one for the **database server**. These servers operate independently.
  
- **Final Project Setup (`vagrant/finalproject/Vagrantfile`)**: (pending).

## Python Packages

To install the required dependencies, run the following commands:

1. `pip install matplotlib`
2. `pip install pandas`
3. `pip install numpy`

## Running the Tests

### For the Midterm Project

Here are the commands to run the tests for the Midterm Project:

- **Load Test**: `python -m tests.load load`  
  Simulates normal traffic to test the system’s performance under expected load.

- **Stress Test**: `python -m tests.load stress`  
  Pushes the system beyond its limits to identify breaking points.

- **Reliability Test**: `python -m tests.reliability`  
  Tests the system’s stability and error rates under sustained load over time.

### For the Final Project

- **Load Balancing Test**: (pending).

## Results

All results are saved in the `results` directory, which is created automatically. Subdirectories for each test type (e.g., `results/load`, `results/stress`, etc.) will be generated. The results are stored in CSV format for easy analysis.

## Charts

Charts for visualizing test results are stored in the `charts` folder. These charts are **hardcoded**, meaning you will need to manually pass the result filename (without the `.csv` extension) as a parameter when running the chart scripts. You may also need to adjust the lines and labels in the chart code depending on your test data and load ranges.

### Example Commands:

- `python ./charts/load_test_chart.py load_2024-11-30_06-14`
- `python ./charts/stress_test_chart.py stress_2024-11-29_10-29`
- `python ./charts/reliability_test_chart.py reliability_2024-12-03_11-09`

## Notes

- If you encounter issues with running the tests or setting up the environment, refer to the relevant sections in the Vagrant or Python documentation.
- Results analysis is important for interpreting system performance and identifying bottlenecks or areas for improvement.
