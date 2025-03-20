import tweepy
import requests
from bs4 import BeautifulSoup
import datetime
import os

# Twitter API credentials (from GitHub Secrets)
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Authenticate with Twitter API
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Function to scrape events & birthdays
def get_this_day_history():
    today = datetime.datetime.now()
    month = today.strftime("%B").lower()
    day = today.day

    url = f"https://www.onthisday.com/day/{month}/{day}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch data")
        return [], []
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract historical events
    events = [event.text for event in soup.select(".event")][:3]
    
    # Extract famous birthdays
    births = [birth.text for birth in soup.select(".birth")][:3]

    print(f"📌 Extracted Events: {events}")
    print(f"🎉 Extracted Birthdays: {births}")

    return events, births

# Format tweet text
def format_tweet():
    events, births = get_this_day_history()
    today = datetime.datetime.now().strftime("%d %B %Y")

    tweet_text = f"📅 This Day That Year: {today}\n\n"

    if events:
        tweet_text += "🎯 Events:\n"
        for event in events:
            tweet_text += f"• {event}\n"

    if births:
        tweet_text += "\n🎉 Famous Birthdays:\n"
        for birth in births:
            tweet_text += f"• {birth}\n"

    tweet_text += f"\n⏳ {datetime.datetime.now().strftime('%H:%M:%S')} IST"

    return tweet_text[:260]  # Ensure tweet is below 260 characters

# Post tweet
def post_tweet():
    tweet_text = format_tweet()
    response = client.create_tweet(text=tweet_text)
    print("✅ Tweet posted:", response)

# Run the bot
if __name__ == "__main__":
    post_tweet()
