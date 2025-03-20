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

    # Wikipedia API with User-Agent fix ✅
    wiki = wikipediaapi.Wikipedia(
        language="en",
        user_agent="YourTwitterBot/1.0 (https://github.com/yourusername/TWTBOT/; contact: youremail@example.com)"
    )

    page_title = f"{month}_{day}"
    page = wiki.page(page_title)

    if not page.exists():
        print("❌ Wikipedia page not found:", page_title)
        return [], []

    events_section = page.section("Events")
    births_section = page.section("Births")

    events = events_section.split("\n") if events_section else []
    births = births_section.split("\n") if births_section else []

    # Filter out empty lines and limit to top 3
    events = [event.strip() for event in events if event.strip()][:3]
    births = [birth.strip() for birth in births if birth.strip()][:3]

    print("📌 Extracted Events:", events)
    print("🎉 Extracted Birthdays:", births)

    return events, births

# Format tweet text
d
