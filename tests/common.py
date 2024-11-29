import numpy as np

def user_journey(session, base_url):
    # Step 1: Open main page
    main_url = f"{base_url}/"
    session.get(main_url)

    # Step 2: Go to login page
    login_url = f"{base_url}/login"
    session.get(login_url)

    # Step 3: Perform the login
    login_url = f"{base_url}/check-login"
    payload = {"email": "onlinenewssite@admin.com", "password": "123456789"}
    session.post(login_url, data=payload)

    # Step 4: Go to posts page
    posts_url = f"{base_url}/admin/post"
    session.get(posts_url)

    # Step 5: Go to post create page
    create_post_url = f"{base_url}/admin/post/create"
    session.get(create_post_url)

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

    # Step 7: Search for the post
    search_url = f"{base_url}/?Search-box=Summary test..."
    session.get(search_url)

def generate_user_load(start=10, max_users=1000, steps=100, growth_rate=0.1):
    """
    Generates a list of user load values that increase over time with a logarithmic growth pattern.

    :param start: Starting number of users.
    :param max_users: Maximum number of users (the upper limit).
    :param steps: Number of steps or time intervals (how many data points).
    :param growth_rate: Rate at which the users increase.
    :return: List of user loads over time.
    """
    # generate time intervals
    time_intervals = np.arange(steps)
    
    # calculate user load using a logarithmic growth formula
    user_load = start + (max_users - start) * np.log1p(growth_rate * time_intervals)
    
    # ensure the user load does not exceed max_users
    user_load = np.clip(user_load, start, max_users)
    
    # round the values 
    user_load = np.round(user_load).astype(int)
    
    return user_load