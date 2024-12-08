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
# Simultaneous threads
max_workers = 5
# Seconds per hour
seconds_per_hour = 3600
# Test duration (hours)
test_duration_hours = 2
# Thread-local storage for session objects
thread_local = threading.local()
#################################################

# Dictionary to hold execution times (response time per user)
test_results = {}


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
        test_result = list(executor.map(test_user_flow, range(num_users)))

    # Store the response times in the global dictionary for logging
    test_results[num_users] = test_result


def test_user_flow(user_id):
    """Simulate a user performing the full flow."""
    journey_sucessful = False
    # Starting time (for each thread)
    start_time = time.time()
    try:

        # Perform the requests to the website
        journey_sucessful = common.user_journey(get_session(), base_url, True)

        # Duration of the thread execution
        duration = time.time() - start_time

    except requests.RequestException as e:
        # Log any request exception (e.g., connection error, timeout, etc.)
        print(f"Error encountered: {user_id}: {e}")

    finally:
        if not journey_sucessful:
            duration = 0  # If there's an error, record it as 0

    return {"start_time": datetime.fromtimestamp(start_time), "duration": duration}


def random_sleep():
    seconds = random.randrange(1, 3)
    time.sleep(seconds)


def get_random_load():
    return random.randrange(5, 90)


if __name__ == "__main__":
    # Prepare the CSV file
    common.prepare_file(output_file)
    # Create the output file and print the header
    with open(output_file, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Elapsed time",
                "Response time",
                "Number of users",
                "Error rate",
                "Elapsed time (global)",
            ]
        )

    # Parameter obtained from the Load Test
    response_time_limit = 1.26

    # Perform the test for 2 hours, randomly triggering a set of requests equivalent to de load (stable)
    launching_time = datetime.now()
    current_time = launching_time
    # Performe the
    while (
        (current_time - launching_time).total_seconds() / seconds_per_hour
    ) < test_duration_hours:
        # Randomize the number of users based on the optimal load range
        num_users = get_random_load()
        perform_test(num_users)

        response_times = test_results[num_users]

        # Filter out None values and calculate the error count
        count_errors = sum(
            1
            for response in response_times
            if response["duration"] == 0 or response["duration"] > response_time_limit
        )
        # Calculate the error rate
        error_rate = (count_errors / num_users) * 100
        # Calculate the elapsed time since the begining of the test
        elapsed_time_global = (datetime.now() - launching_time).total_seconds()
        # Write the results to the CSV file
        with open(output_file, "a", newline="") as file:
            writer = csv.writer(file)
            for response in response_times:
                writer.writerow(
                    [
                        # Calculate the elapsed time since the begining of thread execution
                        (response["start_time"] - launching_time).total_seconds(),
                        response["duration"],
                        num_users,
                        error_rate,
                        elapsed_time_global,
                    ]
                )

        # Sleep randomly to simulate load variation
        random_sleep()
        current_time = datetime.now()

    print(f"Load test completed. Results saved to {output_file}")
