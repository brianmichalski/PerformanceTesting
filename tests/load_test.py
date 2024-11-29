import requests
import time
import threading
import concurrent.futures
import csv
import os
from tests import common

##################### SETUP #####################
# Base URL
base_url = "http://192.168.33.20/OnlineNewsSite"
# Results file
output_file = "results/load_test_results.csv"
# Thread-local storage for session objects
thread_local = threading.local()
#################################################

# Dictionary to hold execution times (response time per user)
execution_time = {}


def get_session():
    """Get a thread-local session."""
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def perform_load_test(num_users):
    """Perform the entire load test using the specified number of users."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Perform all user journeys and then collect response times
        response_times = list(executor.map(test_user_flow, range(num_users)))

    # Store the response times in the global dictionary for logging
    execution_time[num_users] = response_times


def test_user_flow(user_id):
    """Simulate a user performing the full flow."""
    try:
        # Starting time (for each thread)
        start_time = time.time()

        # Perform the requests to the website
        common.user_journey(get_session(), base_url)

        # Duration of the thread execution
        duration = time.time() - start_time

    except requests.RequestException as e:
        # Log any request exception (e.g., connection error, timeout, etc.)
        print(f"Error encountered: {user_id}: {e}")
        duration = None  # If there's an error, record it as None

    return duration


if __name__ == "__main__":
    # Prepare the CSV file with headers (if not already exists)
    try:
        # Delete the output file if it exists
        if os.path.exists(output_file):
            os.remove(output_file)
        # Create the output file and print the header
        with open(output_file, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Number of users", "Response Time (seconds)"])
    except FileExistsError:
        # File already exists, no need to write the header again
        pass

    # Number of simulated users
    numbers = common.generate_user_load(
        start=1, max_users=200, steps=30, growth_rate=0.015
    )

    for num_users in numbers:
        perform_load_test(num_users)

        # Calculate the average response time for the current number of users
        response_times = execution_time[num_users]
        avg_response_time = sum(response_times) / len(response_times)

        # Write the results to the CSV file
        with open(output_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([num_users, avg_response_time])

    print(f"Load test completed. Results saved to {output_file}")
