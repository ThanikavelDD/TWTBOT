import os
import tweepy
import wikipediaapi
from datetime import datetime

# ✅ Authenticate using Twitter API v2 (OAuth 1.0a)
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
)

# ✅ Function to fetch historical events & famous birthdays
def get_this_day_history():
    today = datetime.now().strftime("%B %d")  # e.g., "March 20"
    wiki = wikipediaapi.Wikipedia("en")

    # Fetch Wikipedia page for "March 20"
    page = wiki.page(f"{today}")

    if not page.exists():
        return [], []  # Return empty lists if no data is found

    events, births = [], []
    found_births = False  # Track when "Births" section starts

    # Extract events and births
    for line in page.text.split("\n"):
        if "–" in line:  # Check for event format
            if found_births:
                births.append(line)
            else:
                events.append(line)
        if "Births" in line:
            found_births = True  # Start collecting birthdays

    # Select top 3 events & top 3 birthdays
    top_events = events[:3] if len(events) > 3 else events
    top_births = births[:3] if len(births) > 3 else births

    return top_events, top_births

# ✅ Function to format the tweet (max 260 characters)
def format_tweet():
    events, births = get_this_day_history()
    
    if not events or not births:
        return "📜 This Day That Year 🕰️ - No historical events found for today."

    # Add a timestamp to avoid duplicate tweet errors
    timestamp = datetime.now().strftime("%H:%M")

    tweet = f"📜 This Day That Year 🕰️ ({timestamp} IST)\n\n"

    tweet += "🎂 Famous Birthdays:\n"
    for birth in births:
        tweet += f"• {birth}\n"

    tweet += "\n📌 Key Events:\n"
    for event in events:
        tweet += f"• {event}\n"

    return tweet[:260]  # Ensure it's under 260 characters

# ✅ Function to post the tweet
def post_tweet():
    tweet_text = format_tweet()
    
    try:
        response = client.create_tweet(text=tweet_text)
        print(f"✅ Tweet posted successfully! ID: {response.data['id']}")
    except Exception as e:
        print("❌ Error posting tweet:", e)

# Run the bot
post_tweet()
