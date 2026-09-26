import os
import feedparser
import requests
from datetime import datetime

# Configuration from GitHub Secrets
RSS_URL = os.environ.get("RSS_URL")
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_API_KEY = os.environ.get("BLOGGER_API_KEY")

def get_latest_posts():
    if not RSS_URL:
        print("Error: RSS_URL is not set.")
        return []
    
    feed = feedparser.parse(RSS_URL)
    return feed.entries

def post_to_blogger(title, content, link):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/"
    headers = {
        'Authorization': f'Bearer {BLOGGER_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Adding source link at the end of the post content
    full_content = f"{content}<br><br><a href='{link}'>Read more from original source</a>"
    
    payload = {
        "title": title,
        "content": full_content
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Successfully posted: {title}")
    else:
        print(f"Failed to post {title}: {response.text}")

if __name__ == "__main__":
    entries = get_latest_posts()
    if entries:
        # Posting the latest entry as an example
        latest = entries[0]
        post_to_blogger(latest.title, latest.summary, latest.link)
