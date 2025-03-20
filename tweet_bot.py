import os
import requests
import datetime
import tweepy

# Get today's date
today = datetime.datetime.now().strftime("%B %d")

# Fetch historical events and birthdays
EVENTS_API = "https://history.muffinlabs.com/date"
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

# Authenticate with Twitter API (OAuth 1.0a)
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET"),
)

api = tweepy.API(auth)

# Post the tweet
try:
    api.update_status(tweet_content[:260])  # Ensure within 260 chars
    print("Tweet posted successfully!")
except Exception as e:
    print("Error:", e)
