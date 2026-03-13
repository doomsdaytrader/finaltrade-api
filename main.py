from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Price, News
import scheduler

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="The Final Trade API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    scheduler.start_scheduler()

@app.get("/")
def read_root():
    return {"message": "The Final Trade API - All Glory To God", "status": "online"}

@app.get("/health")
def get_health():
    return {"status": "healthy"}

@app.get("/api/prices")
def get_prices(db: Session = Depends(get_db)):
    prices = db.query(Price).order_by(Price.timestamp.desc()).limit(20).all()
    result = {}
    for p in prices:
        if p.coin_id not in result:
            result[p.coin_id] = {"price_usd": p.price_usd, "timestamp": str(p.timestamp)}
    return result

@app.get("/api/news")
def get_news(category: str = None, db: Session = Depends(get_db)):
    query = db.query(News).order_by(News.timestamp.desc())
    if category:
        query = query.filter(News.category == category)
    news = query.limit(20).all()
    return [{"title": n.title, "category": n.category, "source": n.source, "url": n.url, "timestamp": str(n.timestamp)} for n in news]

@app.get("/api/news/crypto")
def get_crypto_news(db: Session = Depends(get_db)):
    news = db.query(News).filter(News.category == "crypto").order_by(News.timestamp.desc()).limit(10).all()
    return [{"title": n.title, "url": n.url, "timestamp": str(n.timestamp)} for n in news]

@app.get("/api/news/survival")
def get_survival_news(db: Session = Depends(get_db)):
    news = db.query(News).filter(News.category == "survival").order_by(News.timestamp.desc()).limit(10).all()
    return [{"title": n.title, "url": n.url, "timestamp": str(n.timestamp)} for n in news]
