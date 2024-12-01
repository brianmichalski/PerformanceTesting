from datetime import datetime
import os
import numpy as np
from requests import Session


def user_journey(session: Session, base_url, check_response=False):
    # Step 1: Open main page
    main_url = f"{base_url}/"
    response = session.get(main_url)
    if check_response and not response.ok:
        return False

    # Step 2: Go to login page
    login_url = f"{base_url}/login"
    session.get(login_url)
    if check_response and not response.ok:
        return False

    # Step 3: Perform the login
    login_url = f"{base_url}/check-login"
    payload = {"email": "onlinenewssite@admin.com", "password": "123456789"}
    session.post(login_url, data=payload)
    if check_response and not response.ok:
        return False

    # Step 4: Go to posts page
    posts_url = f"{base_url}/admin/post"
    session.get(posts_url)
    if check_response and not response.ok:
        return False

    # Step 5: Go to post create page
    create_post_url = f"{base_url}/admin/post/create"
    session.get(create_post_url)
    if check_response and not response.ok:
        return False

    # Step 6: Save the post (form-data with file upload)
    post_url = f"{base_url}/admin/post/store"
    with open("assets/images/sample.png", "rb") as image_file:
        files = {
            "image": (
                "Harry Potter e a Pedra Filosofal.png",
                image_file,
                "image/png",
            )
        }
        data = {
            "title": "Test Post",
            "cat_id": "15",
            "published_at": "",
            "summary": "Summary test...",
            "body": "Body test...",
        }
        session.post(post_url, data=data, files=files)
    if check_response and not response.ok:
        return False

    # Step 7: Search for the post
    search_url = f"{base_url}/?Search-box=Summary test..."
    session.get(search_url)
    if check_response:
        return response.ok


def generate_user_load(start=1, max_users=1000, steps=100):
    return np.linspace(start, max_users, steps).astype(int)


def prepare_file(path: str):
    # Delete the output file if it exists
    if os.path.exists(path):
        os.remove(path)
    else:
        # Create directories if needed
        os.makedirs(os.path.dirname(path), exist_ok=True)


def get_base_url():
    return "http://192.168.33.20/OnlineNewsSite"


def get_results_filename(script_name):
    curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    test_name = script_name.split(".")[0]
    return f"results/{test_name}/{test_name}_{curr_time}.csv"
