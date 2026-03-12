from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import scheduler

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="The Final Trade API")

# Setup CORS to allow requests from the Next.js dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
def startup_event():
    scheduler.start_scheduler()

@app.get("/")
def read_root():
    return {"message": "Welcome to The Final Trade API"}

@app.get("/health")
def get_health():
    return {"status": "healthy"}
