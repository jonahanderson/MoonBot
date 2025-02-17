import os
import json
import praw
import ftfy
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
        "automoderator", "bot", "cointestmod"
    ]
    return (
        comment.author is not None 
        and comment.author.name.lower() in ['automoderator', 'mod', 'bot', 'cointestmod']
    ) or any(keyword in comment.body.lower() for keyword in automod_keywords)

def fix_text(text):
    try:
        return ftfy.fix_encoding(text)
    except Exception as e:
        print(f"Error fixing text: {e}")
        return text

def fetch_top_and_hot_posts(limit_posts=100, limit_comments=3):
    conversations = []
    system_role_added = False
    
    # Fetch top posts
    top_posts = subreddit.top(time_filter="year", limit=limit_posts)
    # Fetch newest posts
    topmonth_posts = subreddit.top(time_filter="month", limit=limit_posts)

    hot_posts = subreddit.hot(limit=25)

    # Combine the posts
    all_posts = list(top_posts) + list(topmonth_posts) + list(hot_posts)

    for post in all_posts:
        try:
            post_id = post.id
            post_title = fix_text(post.title)
            post_text = fix_text(post.selftext)

            # Fetch the top comments
            post.comments.replace_more(limit=0)
            valid_comments = [
                fix_text(comment.body) for comment in post.comments[:limit_comments] 
                if not isinstance(comment, MoreComments) 
                and not is_automod_comment(comment)
                and comment.body.lower() not in ["[deleted]", "[removed]"]
            ]

            if not valid_comments:
                continue

            # Prepare the data in the chat format
            for i, comment in enumerate(valid_comments):
                if not system_role_added:
                    conversation = {
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant that provides relevant comments to Reddit posts."},
                            {"role": "user", "content": f"{post_title}: {post_text}"},
                            {"role": "assistant", "content": comment}
                        ]
                    }
                    system_role_added = True
                else:
                    conversation = {
                        "messages": [
                            {"role": "user", "content": f"{post_title}: {post_text}"},
                            {"role": "assistant", "content": comment}
                        ]
                    }
                conversations.append(conversation)
        except Exception as e:
            print(f"Error fetching post {post.id}: {e}")

    return conversations

def write_to_jsonl(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for entry in data:
            json.dump(entry, file, ensure_ascii=False)
            file.write('\n')

# Fetch the top and newest posts and comments
top_and_hot_posts_and_comments = fetch_top_and_hot_posts()

# Write the data to a JSONL file
write_to_jsonl(top_and_hot_posts_and_comments, 'reddit_data.jsonl')

print("Data written to reddit_data.jsonl")
