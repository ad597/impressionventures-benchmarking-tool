from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class CompanyStage(str, Enum):
    SEED = "seed"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    SERIES_C = "series_c"
    SERIES_D = "series_d"
    LATE_STAGE = "late_stage"

class Company(BaseModel):
    """Core company model for benchmarking"""
    name: str
    domain: Optional[str] = None
    stage: CompanyStage
    industry: str
    founded_year: Optional[int] = None
    location: Optional[str] = None
    
    # Financial Metrics
    arr: Optional[float] = None
    revenue: Optional[float] = None
    funding_raised: Optional[float] = None
    valuation: Optional[float] = None
    
    # Growth Metrics
    cac: Optional[float] = None  # Customer Acquisition Cost
    ltv: Optional[float] = None  # Lifetime Value
    ltv_cac_ratio: Optional[float] = None
    churn_rate: Optional[float] = None  # Monthly churn rate
    growth_rate: Optional[float] = None  # Monthly growth rate
    
    # Team Metrics
    employee_count: Optional[int] = None
    founders_count: Optional[int] = None
    
    # Additional Data
    description: Optional[str] = None
    business_model: Optional[str] = None
    target_market: Optional[str] = None
    competitive_advantages: Optional[List[str]] = None
    
    # Metadata
    data_sources: List[str] = []
    last_updated: datetime = Field(default_factory=datetime.now)
    confidence_score: Optional[float] = None

class BenchmarkResult(BaseModel):
    """Results from benchmarking analysis"""
    company: Company
    peer_companies: List[Company]
    metrics_comparison: Dict[str, Dict[str, Any]]
    red_flags: List[str]
    insights: List[str]
    risk_score: float  # 0-1 scale
    recommendation: str

class RedFlag(BaseModel):
    """Red flag detection model"""
    flag_type: str
    severity: str  # low, medium, high, critical
    description: str
    metric: str
    value: Any
    threshold: Any
    recommendation: str

class ExtractionResult(BaseModel):
    """Result from LLM extraction pipeline"""
    company_data: Company
    extraction_confidence: float
    missing_fields: List[str]
    extraction_notes: str
