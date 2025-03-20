import tweepy
import wikipediaapi
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

# Function to get historical events and birthdays from Wikipedia
def get_this_day_history():
    today = datetime.datetime.now()
    month = today.strftime("%B")
    day = today.day

    # ✅ Wikipedia API with correct user agent
    wiki = wikipediaapi.Wikipedia(
        language="en",
        user_agent="YourTwitterBot/1.0 (https://github.com/yourusername/TWTBOT/; contact: youremail@example.com)"
    )

    page_title = f"{month} {day}"  # ✅ Correct format
    page = wiki.page(page_title)

    if not page.exists():
        print(f"⚠️ Wikipedia page '{page_title}' not found.")
        return [], []

    lines = page.text.split("\n")
    
    events = []
    births = []
    section = None

    for line in lines:
        line = line.strip()

        if "== Events ==" in line:
            section = "events"
            continue
        elif "== Births ==" in line:
            section = "births"
            continue
        elif "==" in line:
            section = None
            continue

        if section == "events" and len(events) < 3 and len(line) > 10:  # ✅ Ensures text is valid
            events.append(line)
        elif section == "births" and len(births) < 3 and len(line) > 10:  # ✅ Ensures valid text
            births.append(line)

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

    return tweet_text[:260]  # ✅ Ensures tweet is below 260 characters

# Post tweet
def post_tweet():
    tweet_text = format_tweet()
    
    if len(tweet_text.strip()) < 20:  # ✅ Prevents empty tweets
        print("⚠️ No valid data found. Tweet not posted.")
        return
    
    response = client.create_tweet(text=tweet_text)
    print("✅ Tweet posted:", response)

# Run the bot
if __name__ == "__main__":
    post_tweet()
