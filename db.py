# pip{3} install mysql-connector-python
import mysql.connector

# Connect to the DB
mydb = mysql.connector.connect (
    host = "192.168.33.30",
    user = "midterm",
    password = "123456",
    database = "news-project"
)

# Define db Cursor
mycursor = mydb.cursor()

result = mycursor.execute("SELECT COUNT(*) FROM posts")
result = mycursor.fetchone()
total_existing_posts = result[0]

result = mycursor.execute("SELECT COUNT(*) FROM users")
result = mycursor.fetchone()
total_existing_users = result[0]

max_rows = 100000
limit_posts = int(max_rows * 0.2) - total_existing_posts
limit_users = int(max_rows * 0.2) - total_existing_users

print(total_existing_posts, total_existing_users)
print(limit_posts, limit_users)

for i in range(limit_users): 
    email = f"test{total_existing_users+i+1}@examplecom"
    query = """
    INSERT INTO users 
    (username, email, password, permission, is_active, created_at) 
    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP())
    """
    mycursor.execute(query, ('Test', email, '$2y$10$CrqnkHtp2dKlyHfYRniXG.B8fWtrHtfavUyGVqc6bdiiF5lgwzi96', 'user', 1))
    mydb.commit()
   
# Read data from DB
mycursor.execute(f"SELECT COUNT(*)/{max_rows} FROM users")
result = mycursor.fetchall()

# Print results
for table in result:
    print(table)

for i in range(limit_posts): 
    query = """
    INSERT INTO posts 
    (user_id, cat_id, title, summary, body, image, published_at, created_at) 
    VALUES
    (1, 14, 'Test title', 'Test summary', 'Test body', 'public/post-image/2022-10-24-18-38-25.webp', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())
    """
    mycursor.execute(query)
    mydb.commit()
    
# Read data from DB
mycursor.execute(f"SELECT COUNT(*)/{max_rows} FROM posts")
result = mycursor.fetchall()

# Print results
for table in result:
    print(table)

