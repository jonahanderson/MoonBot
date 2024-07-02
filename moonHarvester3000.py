import subprocess
import sys
import time
import pkg_resources

# Function to check if a package is installed
def check_package(package):
    try:
        dist = pkg_resources.get_distribution(package)
        return True
    except pkg_resources.DistributionNotFound:
        return False

# List of required packages
required_packages = ['praw', 'python-dotenv', 'colorama']

# Check and prompt for missing packages
for package in required_packages:
    if not check_package(package):
        print(f"The required package '{package}' is not installed.")
        install = input(f"Do you want to install '{package}' now? (yes/no): ")
        if install.lower() in ['yes', 'y']:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        else:
            print(f"Please install '{package}' manually and re-run the script.")
            sys.exit(1)

import praw
import random
import datetime
import os
import logging
from dotenv import load_dotenv
from colorama import init, Fore, Style

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

# Fetch Reddit credentials from environment variables
userAgent = os.getenv('REDDIT_USER_AGENT')
cID = os.getenv('REDDIT_CLIENT_ID')
cSC = os.getenv('REDDIT_CLIENT_SECRET')
userN = os.getenv('REDDIT_USERNAME')
userP = os.getenv('REDDIT_PASSWORD')

logging.info("Starting Reddit bot")
time.sleep(1)  # Adding a delay for readability

# Initialize Reddit instance
reddit = praw.Reddit(
    user_agent=userAgent,
    client_id=cID,
    client_secret=cSC,
    username=userN,
    password=userP
)

subreddit = reddit.subreddit('cryptocurrency')

def process_submission(submission):
    logging.info(f"Processing submission: {submission.title}")
    print(f"{Fore.CYAN}Title:{Style.RESET_ALL} {submission.title}")
    print(f"{Fore.CYAN}Text:{Style.RESET_ALL} {submission.selftext}")
    print(f"{Fore.CYAN}Karma:{Style.RESET_ALL} {submission.score}")
    print(f"{Fore.CYAN}SUBMISSION ID:{Style.RESET_ALL} {submission.id}")
    print(f"{Fore.CYAN}DATE AND TIME:{Style.RESET_ALL} {datetime.datetime.fromtimestamp(int(submission.created)).strftime('%Y-%m-%d %H:%M:%S')}")
    print(" --- ")

    x = input(f"{Fore.YELLOW}Enter your comment:{Style.RESET_ALL} ")

    if x == "SKIP":
        submission.save()
        logging.info("Skipping this post")
        print(f"{Fore.YELLOW}SKIPPING THIS POST{Style.RESET_ALL}")
    else:
        try:
            logging.info(f"Posting comment: {x}")
            submission.reply(x)
            submission.save()
            logging.info("Comment posted successfully")
            print(f"{Fore.GREEN}Comment Posted{Style.RESET_ALL}")
        except praw.exceptions.APIException as e:
            logging.error(f"An error occurred: {e}")
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

try:
    # Fetch recent posts
    logging.info("Fetching latest submissions")
    time.sleep(1)  # Adding a delay for readability
    for submission in subreddit.new(limit=10):  # Adjust the limit as needed
        process_submission(submission)
        print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")  # Adding a separator for readability

    # Stream new submissions
    logging.info("Starting subreddit stream")
    start_time = time.time()
    time.sleep(1)  # Adding a delay for readability
    for submission in subreddit.stream.submissions(skip_existing=True):
        if not submission.saved and not submission.created_utc < start_time:
            process_submission(submission)
            print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")  # Adding a separator for readability
            # Random delay to mimic human behavior
            time.sleep(random.randint(2, 10))
except Exception as e:
    logging.error(f"An error occurred: {e}")
    print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
