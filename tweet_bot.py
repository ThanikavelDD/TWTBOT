import os
import requests
import datetime
import random
import tweepy

# Get today's date
today = datetime.datetime.now().strftime("%B %d")

# Fetch historical events and birthdays (example API, replace with actual source)
EVENTS_API = f"https://history.muffinlabs.com/date"
response = requests.get(EVENTS_API).json()

# Extract top 3 historical events
events = response["data"]["Events"][:3]
events_text = [f"{e['year']}: {e['text']}" for e in events]

# Extract top 3 famous birthdays
birthdays = response["data"]["Births"][:3]
birthdays_text = [f"{b['year']}: {b['text']}" for b in birthdays]

# Format the tweet (under 260 characters)
tweet_content = f"📜 This Day That Year ({today}) 📜\n\n"
tweet_content += "🎉 Birthdays:\n" + "\n".join(birthdays_text) + "\n\n"
tweet_content += "📖 Events:\n" + "\n".join(events_text) + "\n\n"
tweet_content += f"⏳ {datetime.datetime.now().strftime('%H:%M:%S')} IST"  # Add timestamp

# Authenticate with Twitter API
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

# Post the tweet
try:
    client.create_tweet(text=tweet_content[:260])  # Ensure within 260 chars
    print("Tweet posted successfully!")
except Exception as e:
    print("Error:", e)
