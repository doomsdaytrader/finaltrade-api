import feedparser
from sqlalchemy.orm import Session
from models import News

RSS_FEEDS = {
    "crypto": [
        "https://cointelegraph.com/rss",
        "https://cryptoslate.com/feed/"
    ],
    "survival": [
        "https://www.reuters.com/world/rss",
        "https://apnews.com/hub/ap-top-news?output=rss"
    ]
}

def fetch_rss(db: Session):
    for category, urls in RSS_FEEDS.items():
        for url in urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:  # Get top 5 from each feed
                    # Check if exists
                    existing = db.query(News).filter(News.url == entry.link).first()
                    if not existing:
                        news_item = News(
                            title=entry.title,
                            category=category,
                            source=url,
                            url=entry.link
                        )
                        db.add(news_item)
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                
    db.commit()
