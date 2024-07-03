import openai
import logging
from dotenv import load_dotenv
import os
import sys
import praw
import datetime
import sqlite3
from colorama import init, Fore, Style
import time

# Ensure Python version is 3.8 or above
assert sys.version_info >= (3, 8), "Please use Python 3.8 or above."

# Initialize colorama
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Configure logging to write to the console with colors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Custom logging levels with color
class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            record.msg = f"{Fore.GREEN}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Apply custom formatter
for handler in logging.getLogger().handlers:
    handler.setFormatter(CustomFormatter('%(asctime)s - %(levelname)s - %(message)s'))

# Fetch credentials and API keys from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
userAgent = os.getenv('REDDIT_USER_AGENT')
cID = os.getenv('REDDIT_CLIENT_ID')
cSC = os.getenv('REDDIT_CLIENT_SECRET')
userN = os.getenv('REDDIT_USERNAME')
userP = os.getenv('REDDIT_PASSWORD')

logging.info("Starting Moon Bot...\n")
time.sleep(1)  # Adding a delay for readability
print(f"{Fore.MAGENTA}{'='*2}{Style.RESET_ALL}")

# Initialize Reddit instance
reddit = praw.Reddit(
    user_agent=userAgent,
    client_id=cID,
    client_secret=cSC,
    username=userN,
    password=userP
)

subreddit = reddit.subreddit('cryptocurrency')

# Initialize SQLite database and cursor
conn = sqlite3.connect('moonbot.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS processed_posts (
    id TEXT PRIMARY KEY,
    title TEXT,
    selftext TEXT,
    created_utc INTEGER
)
''')
conn.commit()

def is_post_processed(post_id):
    c.execute('SELECT id FROM processed_posts WHERE id = ?', (post_id,))
    return c.fetchone() is not None

def mark_post_as_processed(submission):
    c.execute('INSERT INTO processed_posts (id, title, selftext, created_utc) VALUES (?, ?, ?, ?)', 
              (submission.id, submission.title, submission.selftext, submission.created_utc))
    conn.commit()

def generate_comments(post_title, post_text):
    prompt = f"Generate a comment for the following Reddit post:\n\nTitle: {post_title}\n\nText: {post_text}\n\nPlease ensure the comment is in lowercase, does not contain quotes, and does not contain any emojis."
    
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a versatile Reddit commenter aiming to maximize karma on the cryptocurrency subreddit. Your comments should be engaging and tailored to the context—sometimes informative, sometimes humorous or sarcastic, and occasionally provocative. Always consider what type of comment will get the most upvotes in each situation. Ensure the comments are in lowercase and do not include any emojis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=1.0,  # Increased temperature for more variability
            n=3  # Request three completions
        )
        comments = [choice.message.content.strip() for choice in completion.choices]
        return comments
    except openai.RateLimitError as e:
        logging.error(f"Rate limit error: {e}")
        return []
    except openai.AuthenticationError as e:
        logging.error(f"Authentication error: {e}")
        return []
    except openai.APIConnectionError as e:
        logging.error(f"API connection error: {e}")
        return []
    except openai.OpenAIError as e:
        logging.error(f"OpenAI error: {e}")
        return []
    except Exception as e:
        logging.error(f"An unknown error occurred while generating comments: {e}")
        return []

def process_submission(submission):
    if is_post_processed(submission.id):
        logging.info(f"Skipping already processed submission:{Fore.YELLOW} {submission.title}")
        return

    logging.info(f"Processing submission ID {submission.id}...")
    print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
    time.sleep(1)
    print(f"{Fore.CYAN}Title:{Fore.YELLOW} {submission.title}")
    print(f"{Fore.CYAN}Text:{Style.RESET_ALL}\n{submission.selftext}\n")
    print(f"{Fore.CYAN}Karma:{Style.RESET_ALL} {submission.score}")
    print(f"{Fore.CYAN}SUBMISSION ID:{Style.RESET_ALL} {submission.id}")
    print(f"{Fore.CYAN}DATE AND TIME:{Style.RESET_ALL} {datetime.datetime.fromtimestamp(int(submission.created)).strftime('%Y-%m-%d %H:%M:%S')}")
    print(" --- ")

    # Store the submission data
    mark_post_as_processed(submission)

    while True:
        x = input(f"{Fore.YELLOW}Enter your comment (or type 'g' to generate potential comments, 's' to skip this post): {Style.RESET_ALL} ")

        if x.lower() == "s":
            logging.info("Skipping this post")
            print(f"{Fore.YELLOW}SKIPPING THIS POST{Style.RESET_ALL}")
            break
        elif x.lower() == "g":
            while True:
                comments = generate_comments(submission.title, submission.selftext)
                if comments:
                    print(" --- ")
                    for i, comment in enumerate(comments, start=1):
                        print(f"{Fore.YELLOW}Generated Comment {i}:{Style.RESET_ALL} {comment}")
                        if i < len(comments):  # Add a new line between comments
                            print("\n")

                    print(" --- ")
                    choice = input(f"{Fore.YELLOW}Choose a comment to post: 1, 2, 3 ('b' to go back, 'g' to generate new comments): {Style.RESET_ALL} ")
                    
                    if choice in ['1', '2', '3']:
                        selected_comment = comments[int(choice) - 1]
                        confirm = input(f"{Fore.YELLOW}Are you sure you want to post this comment? (y/n): {Style.RESET_ALL}")
                        if confirm.lower() == 'y':
                            try:
                                logging.info(f"Posting generated comment: {selected_comment}")
                                submission.reply(selected_comment)
                                time.sleep(1)
                                logging.info("Generated comment posted successfully")
                                print(f"{Fore.GREEN}Generated Comment Posted{Style.RESET_ALL}")
                                time.sleep(1)
                                break
                            except praw.exceptions.APIException as e:
                                logging.error(f"An error occurred: {e}")
                                print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
                        elif confirm.lower() == 'n':
                            print(f"{Fore.YELLOW}Comment not posted. Choose another comment or generate new comments.{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
                    elif choice.lower() == 'b':
                        break  # Break out to allow manual comment entry
                    elif choice.lower() == 'g':
                        continue  # Continue to generate new comments
                    else:
                        print(f"{Fore.RED}Invalid choice. Please select 1, 2, 3, 'b', or 'g'.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to generate comments. Please try again.{Style.RESET_ALL}")
        else:
            try:
                confirm = input(f"{Fore.YELLOW}Are you sure you want to post this comment? (y/n): {Style.RESET_ALL}")
                if confirm.lower() == 'y':
                    submission.reply(x)
                    logging.info(f"User comment posted successfully: {x}")
                    time.sleep(1)
                    print(f"{Fore.GREEN}User Comment Posted{Style.RESET_ALL}")
                    break
                elif confirm.lower() == 'n':
                    print(f"{Fore.YELLOW}Comment not posted. Enter another comment or generate new comments.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
            except praw.exceptions.APIException as e:
                logging.error(f"An error occurred: {e}")
                print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

def fetch_recent_posts():
    logging.info("Fetching latest submissions")
    time.sleep(1)
    for submission in subreddit.new(limit=20):  # Adjust the limit as needed
        process_submission(submission)
        print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")  # Adding a separator for readability
        time.sleep(1)


def stream_new_submissions():
    logging.info("Starting subreddit stream")
    print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
    time.sleep(1)
    print(f"{Fore.GREEN}Live posts will come automatically below once posted.")
    start_time = time.time()
    for submission in subreddit.stream.submissions(skip_existing=True):
        if not is_post_processed(submission.id):
            process_submission(submission)
            print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")  # Adding a separator for readability
            time.sleep(1)

def fetch_then_stream():
    fetch_recent_posts()
    stream_new_submissions()

def clear_database():
    c.execute('DELETE FROM processed_posts')
    conn.commit()
    print(f"{Fore.RED}Database cleared!{Style.RESET_ALL}")

def main():
    print(f"{Fore.YELLOW}Welcome to the Moon Bot!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Choose an option:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Fetch recent posts{Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. Stream new submissions{Style.RESET_ALL}")
    print(f"{Fore.GREEN}3. Fetch 20 recent posts and then stream new submissions{Style.RESET_ALL}")
    print(f"{Fore.GREEN}4. Clear processed posts database{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*2}\n{Style.RESET_ALL}")
    choice = input(f"{Fore.YELLOW}Enter your choice (1, 2, 3, or 4): {Style.RESET_ALL}")

    if choice == '1':
        fetch_recent_posts()
    elif choice == '2':
        stream_new_submissions()
    elif choice == '3':
        fetch_then_stream()
    elif choice == '4':
        clear_database()
    else:
        print(f"{Fore.RED}Invalid choice. Please run the script again and select a valid option.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
    finally:
        conn.close()  # Ensure the database connection is closed
