import os
import feedparser
import requests

# GitHub Secrets se credentials uthana
API_KEY = os.getenv("BLOGGERAPIKEY")
BLOG_ID = os.getenv("BLOGGER_BLOG_ID")
RSS_URL = os.getenv("RSS_URL")

def post_to_blogger(title, content, url):
    endpoint = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    
    # Content ko unique aur clean banane ke liye formatting
    formatted_content = f"""
    <p>{content}</p>
    <br>
    <hr>
    <p><em>Source: Global News Desk</em></p>
    """
    
    payload = {
        "title": title,
        "content": formatted_content
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Agar Blogger API key Bearer ki jagah query parameter (key=...) use karti hai toh endpoint adjust karein:
    # Yahan hum standard OAuth/API key format use kar rahe hain
    response = requests.post(f"{endpoint}?key={API_KEY}", json=payload)
    if response.status_code == 200:
        print(f"Successfully posted: {title}")
    else:
        print(f"Failed to post: {response.text}")

def main():
    if not RSS_URL:
        print("RSS URL not found!")
        return

    feed = feedparser.parse(RSS_URL)
    
    # Sabse latest news ko uthana
    if feed.entries:
        latest_entry = feed.entries[0]
        title = latest_entry.title
        summary = latest_entry.get("summary", latest_entry.get("description", ""))
        link = latest_entry.link
        
        print(f"Processing news: {title}")
        post_to_blogger(title, summary, link)

if __name__ == "__main__":
    main()
    
