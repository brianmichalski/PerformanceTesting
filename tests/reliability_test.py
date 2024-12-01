import concurrent.futures
import csv
from datetime import datetime
import os
import random
import requests
import time
from tests import common
import threading


##################### SETUP #####################
# Base URL
base_url = common.get_base_url()
# Results file
output_file = common.get_results_filename(os.path.basename(__file__))
# Thread-local storage for session objects
thread_local = threading.local()
# Simultaneous threads
max_workers = 5
# Seconds per hour
seconds_per_hour = 3600
# Test duration (hours)
test_duration_hours = 2
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
    """Simulate a user performing the full flow."""
    journey_sucessful = False
    try:
        # Starting time (for each thread)
        start_time = time.time()

        # Perform the requests to the website
        journey_sucessful = common.user_journey(get_session(), base_url, True)

        # Duration of the thread execution
        duration = time.time() - start_time

    except requests.RequestException as e:
        # Log any request exception (e.g., connection error, timeout, etc.)
        print(f"Error encountered: {user_id}: {e}")

    finally:
        if not journey_sucessful:
            duration = None  # If there's an error, record it as None

    return duration


def random_sleep():
    minutes = random.randrange(5, 15)
    time.sleep(minutes * 60)


if __name__ == "__main__":
    # Prepare the CSV file
    common.prepare_file(output_file)
    # Create the output file and print the header
    with open(output_file, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Number of users", "Error rate", "Actual Number of Users"])

    # Parameters obtained from the Load Test
    response_time_limit = 1.5
    max_num_users = 200

    # Perform the test for 2 hours, randomly triggering a set of requests equivalent to de load (stable)
    launching_time = datetime.now()
    elapsed_time = launching_time
    # Performe the
    while (
        (elapsed_time - launching_time).total_seconds() / seconds_per_hour
    ) < test_duration_hours:
        # todo: randomize the number of users based on the maximum
        num_users = max_num_users
        perform_test(num_users)

        # Calculate the average response time for the current number of users
        response_times = execution_time[num_users]
        count_errors = sum(
            1
            for response in response_times
            if response is None or response > response_time_limit
        )
        error_rate = count_errors / num_users
        actual_num_users = len(response_times)

        # Write the results to the CSV file
        with open(output_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([num_users, count_errors, actual_num_users])

        random_sleep()
        elapsed_time = datetime.now()

    print(f"Load test completed. Results saved to {output_file}")
