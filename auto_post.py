import praw
import feedparser
import os
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
from colorama import init, Fore, Style


# Load environment variables
load_dotenv()

REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

# Initialize PRAW with your credentials
reddit = praw.Reddit(
    user_agent=REDDIT_USER_AGENT,
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
)

# List of RSS feed URLs
rss_feeds = [
    "https://cryptobriefing.com/feed/",
    "https://dailyhodl.com/feed/",
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml",
    "https://www.newsbtc.com/feed/",
    "https://www.crypto-news-flash.com/feed/",
    "https://cryptopotato.com/feed/",
    "https://www.theblock.co/rss",
    "https://decrypt.co/feed",

]

# Function to fetch new articles
def fetch_new_articles(rss_feeds):
    new_articles = []
    utc = pytz.utc
    for feed in rss_feeds:
        parsed_feed = feedparser.parse(feed)
        for entry in parsed_feed.entries:
            published = datetime(*entry.published_parsed[:6], tzinfo=utc)
            new_articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': published
            })
    # Sort articles by published date in descending order
    new_articles = sorted(new_articles, key=lambda x: x['published'], reverse=True)
    return new_articles[:10]  # Return top 10 articles

# Function to get the flair ID based on flair text
def get_flair_id(subreddit, flair_text):
    for flair in subreddit.flair.link_templates:
        if flair['text'].lower() == flair_text.lower():
            return flair['id']
    raise ValueError(f"Flair '{flair_text}' not found")

# Function to post to Reddit
def post_to_reddit(article, flair_text):
    subreddit = reddit.subreddit("cryptocurrency")
    flair_id = get_flair_id(subreddit, flair_text)
    subreddit.submit(article['title'], url=article['link'], flair_id=flair_id)
    print(f"{Fore.GREEN}Posted: {article['title']}")

# Main function
def main():
    flair_text = "GENERAL-NEWS"  # Replace with the actual flair text
    articles = fetch_new_articles(rss_feeds)
    
    # Timezone conversion
    eastern = pytz.timezone('US/Eastern')
    
    # Display the top 10 articles
    print(f"\n")
    for idx, article in enumerate(articles, start=1):
        eastern_time = article['published'].astimezone(eastern)
        formatted_time = eastern_time.strftime('%Y-%m-%d %I:%M:%S %p %Z')
        print(f"{Fore.YELLOW}Article {idx}: {Fore.CYAN}{article['title']}\nTIME: {Style.RESET_ALL}{formatted_time}\n{Fore.CYAN}LINK: {Style.RESET_ALL}{article['link']}\n")

    # Get user input to select an article
    while True:
        try:
            choice = int(input("Enter the article number to post (1-10): "))
            if 1 <= choice <= 10:
                selected_article = articles[choice - 1]
                post_to_reddit(selected_article, flair_text)
                break
            else:
                print("Invalid input. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()
