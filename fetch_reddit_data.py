import os
import json
import praw
from dotenv import load_dotenv
from praw.models import MoreComments

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

def is_automod_comment(comment):
    automod_keywords = [
        "automoderator", "bot"
    ]
    return (comment.author is not None and comment.author.name.lower() in ['automoderator', 'mod', 'bot']) or any(keyword in comment.body.lower() for keyword in automod_keywords)

def decode_unicode_escape(text):
    try:
        return text.encode('latin1').decode('unicode_escape')
    except:
        return text

def fetch_top_and_hot_posts(limit_posts=50, limit_hot_posts=10, limit_comments=1):
    posts_data = []
    
    # Fetch top posts
    top_posts = subreddit.top(time_filter="year", limit=limit_posts)
    # Fetch newest posts
    hot_posts = subreddit.hot(limit=limit_hot_posts)

    # Combine the posts
    all_posts = list(top_posts) + list(hot_posts)

    for post in all_posts:
        try:
            post_id = post.id
            post_title = decode_unicode_escape(post.title)
            post_text = decode_unicode_escape(post.selftext)

            # Fetch the top comments
            post.comments.replace_more(limit=0)
            top_comments = [
                decode_unicode_escape(comment.body) for comment in post.comments[:limit_comments] 
                if not isinstance(comment, MoreComments) 
                and not is_automod_comment(comment)
                and comment.body.lower() not in ["[deleted]", "[removed]"]
            ]

            # Prepare the data in the chat format
            for comment in top_comments:
                post_data = {
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant that provides relevant comments to Reddit posts."},
                        {"role": "user", "content": f"Post Title: {post_title}\nPost Text: {post_text}"},
                        {"role": "assistant", "content": comment}
                    ]
                }
                posts_data.append(post_data)
        except Exception as e:
            print(f"Error fetching post {post.id}: {e}")

    return posts_data

def write_to_jsonl(data, filename):
    with open(filename, 'w') as file:
        for entry in data:
            json.dump(entry, file)
            file.write('\n')

# Fetch the top and newest posts and comments
top_and_hot_posts_and_comments = fetch_top_and_hot_posts()

# Write the data to a JSONL file
write_to_jsonl(top_and_hot_posts_and_comments, 'reddit_data.jsonl')

print("Data written to reddit_data.jsonl")
