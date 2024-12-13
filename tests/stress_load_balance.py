import concurrent.futures
import csv
import requests
import statistics
import time
from tests import common
import threading

##################### SETUP #####################
# Results file
output_file = common.get_results_filename('stress_load_balance')
# Thread-local storage for session objects
thread_local = threading.local()
# Simultaneous threads
max_workers = 5
# Number of simulated users (threads)
users_list = [ 1, 2, 3, 4, 5, 6, 10, 16, 21, 27, 32, 37, 42, 47, 53, 58, 63, 68, 73, 79,
              84, 89, 94, 100, 119, 144, 170, 196, 221, 247, 273, 298, 324, 350, 369, 439, 
              509, 579, 649, 719, 789, 859, 929, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 
              2750, 3000]
servers = ['192.168.33.20','192.168.33.30']
relative_path = 'OnlineNewsSite'
#################################################

# Dictionary to hold execution times (response time per user)
execution_time = {}


def get_session():
    """Get a thread-local session."""
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def perform_test(num_users):
    """Perform the entire load test using the specified number of users."""
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers, thread_name_prefix=f"{num_users}_"
    ) as executor:
        # Perform all user journeys and then collect response times
        response_times = list(executor.map(test_user_flow, range(num_users)))

    # Store the response times in the global dictionary for logging
    execution_time[num_users] = response_times


def test_user_flow(user_id):
    # Basic server switching for load balacing
    server = servers[user_id % 2]
    
    """Simulate a user performing the full flow."""
    # Starting time (for each thread)
    start_time = time.time()
    try:
        # Perform the requests to the website
        common.user_journey(get_session(), f"http://{server}/{relative_path}")
    except requests.RequestException as e:
        # Log any request exception (e.g., connection error, timeout, etc.)
        print(f"Error encountered: {user_id}: {e}")

    finally:
        # Duration of the thread execution
        duration = time.time() - start_time

    return duration


if __name__ == "__main__":
    # Prepare the CSV file with headers (if not already exists)
    common.prepare_file(output_file)
    # Create the output file and print the header
    with open(output_file, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Number of users",
                "AVG Response Time",
                "Median Response Time",
            ]
        )

    for num_users in users_list:
        perform_test(num_users)

        # Calculate the average response time for the current number of users
        response_times = execution_time[num_users]
        avg_response_time = sum(response_times) / len(response_times)
        median_response_time = statistics.median(response_times)

        # Write the results to the CSV file
        with open(output_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [num_users, avg_response_time, median_response_time]
            )

    print(f"Load test completed. Results saved to {output_file}")
