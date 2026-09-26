import os
import feedparser
import requests

CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")
BLOG_ID = os.getenv("BLOGGER_BLOG_ID")
RSS_URL = os.getenv("RSS_URL")

def post_to_blogger(title, content, url):
    endpoint = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    
    formatted_content = f"""
    <p>{content}</p>
    <br>
    <hr>
    <p><em>Source: <a href="{url}">Global News Desk</a></em></p>
    """
    
    payload = {
        "title": title,
        "content": formatted_content
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Direct request using client keys
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    response = requests.post(endpoint, json=payload, headers=headers, params=params)
    if response.status_code == 200:
        print(f"Successfully posted: {title}")
    else:
        print(f"Failed to post: {response.text}")

def main():
    if not RSS_URL:
        print("RSS URL not found!")
        return
        
    feed = feedparser.parse(RSS_URL)
    
    if feed.entries:
        latest_entry = feed.entries[0]
        title = latest_entry.title
        summary = latest_entry.get("summary", latest_entry.get("description", ""))
        link = latest_entry.link
        
        print(f"Processing news: {title}")
        post_to_blogger(title, summary, link)

if __name__ == "__main__":
    main()
