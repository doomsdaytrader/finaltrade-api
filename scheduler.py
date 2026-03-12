from apscheduler.schedulers.background import BackgroundScheduler
import services.news_fetcher as news_fetcher
import services.crypto_fetcher as crypto_fetcher
from database import SessionLocal

scheduler = BackgroundScheduler()

def fetch_and_store_news():
    print("Fetching news...")
    db = SessionLocal()
    try:
        news_fetcher.fetch_rss(db)
    finally:
        db.close()
    print("Done fetching news.")

def fetch_and_store_crypto():
    print("Fetching crypto prices...")
    db = SessionLocal()
    try:
        crypto_fetcher.fetch_prices(db)
    finally:
        db.close()
    print("Done fetching crypto.")

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(fetch_and_store_crypto, 'interval', minutes=1, id='crypto_job_id', replace_existing=True)
        scheduler.add_job(fetch_and_store_news, 'interval', minutes=5, id='news_job_id', replace_existing=True)
        scheduler.start()
        print("Scheduler started!")
