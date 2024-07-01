#!/usr/bin/python
import praw
import random
import time
import datetime
import os
import logging

# Configure logging
logging.basicConfig(filename='reddit_bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Fetch Reddit credentials from environment variables
userAgent = os.getenv('REDDIT_USER_AGENT')
cID = os.getenv('REDDIT_CLIENT_ID')
cSC = os.getenv('REDDIT_CLIENT_SECRET')
userN = os.getenv('REDDIT_USERNAME')
userP = os.getenv('REDDIT_PASSWORD')

reddit = praw.Reddit(user_agent=userAgent, client_id=cID, client_secret=cSC, username=userN, password=userP)
subreddit = reddit.subreddit('cryptocurrency')

start_time = time.time()  # Only look at new submissions after the stream starts

for submission in subreddit.stream.submissions():
    if not submission.saved and not submission.created_utc < start_time:
        print(" ")
        print('*NEW SUBMISSION*')
        print("Title: ", submission.title)
        print(" ")
        print("Text: ", submission.selftext)
        print(" --- ")
        print("Karma: ", submission.score)
        print("SUBMISSION ID: ", submission.id)
        print("SUBMISSION SAVED?: ", submission.saved)
        print("DATE AND TIME: ", datetime.datetime.fromtimestamp(int(submission.created)).strftime('%Y-%m-%d %H:%M:%S'))
        print(" --- ")

        x = input("Enter your comment: ")

        print(" ")
        if x == "SKIP":
            submission.save()
            print("SKIPPING THIS POST")
        else:
            try:
                print('Posting Comment: ', x)
                submission.reply(x)
                submission.save()
                logging.info('Comment Posted: %s', x)
                print("")
                print("Comment Posted")
                print("")
            except praw.exceptions.APIException as e:
                logging.error(f"An error occurred: {e}")
                print(f"An error occurred: {e}")

        print('GOING TO NEXT POST')
        print("NEW POST -------------------------------------------------------------------------------------- NEW POST")

        # Random delay to mimic human behavior
        time.sleep(random.randint(2, 10))
