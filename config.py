import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY")
    LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///benchmarking.db")
    
    # Model Configuration
    DEFAULT_MODEL = "gpt-4-turbo-preview"
    EMBEDDING_MODEL = "text-embedding-3-small"
    
    # Vector Database
    FAISS_INDEX_PATH = "data/faiss_index"
    
    # Benchmarking thresholds
    ARR_THRESHOLD = 1000000  # $1M ARR
    CAC_THRESHOLD = 5000     # $5K CAC
    LTV_THRESHOLD = 50000    # $50K LTV
    CHURN_THRESHOLD = 0.05   # 5% monthly churn
