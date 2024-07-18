import os
import json
import praw
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch credentials and API keys from environment variables
userAgent = os.getenv('REDDIT_USER_AGENT')
cID = os.getenv('REDDIT_CLIENT_ID')
cSC = os.getenv('REDDIT_CLIENT_SECRET')
userN = os.getenv('REDDIT_USERNAME')
userP = os.getenv('REDDIT_PASSWORD')

# Initialize Reddit instance
reddit = praw.Reddit(
    user_agent=userAgent,
    client_id=cID,
    client_secret=cSC,
    username=userN,
    password=userP
)

subreddit = reddit.subreddit('cryptocurrency')

def fetch_top_posts_and_comments():
    posts_data = []
    top_posts = subreddit.top(limit=20)

    for post in top_posts:
        post_id = post.id
        post_title = post.title
        post_text = post.selftext

        # Fetch the top 2 comments
        post.comments.replace_more(limit=0)
        top_comments = [comment.body for comment in post.comments[:2]]

        # Prepare the data
        post_data = {
            "prompt": f"Post Title: {post_title}\nPost Text: {post_text}",
            "completion": " ".join(top_comments)
        }
        posts_data.append(post_data)

    return posts_data

def write_to_jsonl(data, filename):
    with open(filename, 'w') as file:
        for entry in data:
            json.dump(entry, file)
            file.write('\n')

# Fetch the top posts and comments
top_posts_and_comments = fetch_top_posts_and_comments()

# Write the data to a JSONL file
write_to_jsonl(top_posts_and_comments, 'reddit_data.jsonl')

print("Data written to reddit_data.jsonl")
