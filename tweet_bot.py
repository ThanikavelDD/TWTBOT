import os
import tweepy

# Authenticate using Twitter API v2
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
)

# Test Tweet
try:
    response = client.create_tweet(text="Hello, Twitter API v2! 🚀")
    print(f"✅ Tweet posted successfully! ID: {response.data['id']}")
except Exception as e:
    print("❌ Error posting tweet:", e)
