import faiss
import numpy as np
import pickle
import json
from typing import List, Dict, Any, Tuple
from sklearn.preprocessing import StandardScaler
from models import Company
from config import Config
import os

class CompanyVectorizer:
    """Convert company data to vectors for similarity search"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []
        self._setup_features()
    
    def _setup_features(self):
        """Define which features to use for vectorization"""
        self.feature_names = [
            'arr', 'revenue', 'funding_raised', 'valuation',
            'cac', 'ltv', 'ltv_cac_ratio', 'churn_rate', 'growth_rate',
            'employee_count', 'founders_count', 'founded_year'
        ]
    
    def company_to_vector(self, company: Company) -> np.ndarray:
        """Convert company to numerical vector"""
        features = []
        
        # Financial metrics
        features.append(company.arr or 0)
        features.append(company.revenue or 0)
        features.append(company.funding_raised or 0)
        features.append(company.valuation or 0)
        
        # Growth metrics
        features.append(company.cac or 0)
        features.append(company.ltv or 0)
        features.append(company.ltv_cac_ratio or 0)
        features.append(company.churn_rate or 0)
        features.append(company.growth_rate or 0)
        
        # Team metrics
        features.append(company.employee_count or 0)
        features.append(company.founders_count or 0)
        
        # Time-based features
        current_year = 2024
        founded_year = company.founded_year or current_year
        features.append(current_year - founded_year)  # Company age
        
        return np.array(features, dtype=np.float32)
    
    def companies_to_vectors(self, companies: List[Company]) -> np.ndarray:
        """Convert list of companies to matrix of vectors"""
        vectors = []
        for company in companies:
            vector = self.company_to_vector(company)
            vectors.append(vector)
        
        return np.vstack(vectors)
    
    def fit_scaler(self, vectors: np.ndarray):
        """Fit the scaler on the training data"""
        self.scaler.fit(vectors)
    
    def transform_vectors(self, vectors: np.ndarray) -> np.ndarray:
        """Scale vectors using fitted scaler"""
        return self.scaler.transform(vectors)

class CompanyVectorDatabase:
    """FAISS-based vector database for company similarity search"""
    
    def __init__(self, dimension: int = 12):
        self.dimension = dimension
        self.index = None
        self.companies = []
        self.vectorizer = CompanyVectorizer()
        self.is_trained = False
    
    def add_companies(self, companies: List[Company]):
        """Add companies to the database"""
        self.companies.extend(companies)
        
        # Convert to vectors
        vectors = self.vectorizer.companies_to_vectors(companies)
        
        if not self.is_trained:
            # First time - fit scaler and create index
            self.vectorizer.fit_scaler(vectors)
            scaled_vectors = self.vectorizer.transform_vectors(vectors)
            
            # Create FAISS index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(scaled_vectors.astype(np.float32))
            self.is_trained = True
        else:
            # Add to existing index
            scaled_vectors = self.vectorizer.transform_vectors(vectors)
            self.index.add(scaled_vectors.astype(np.float32))
    
    def search_similar(self, query_company: Company, k: int = 10) -> List[Tuple[Company, float]]:
        """Find k most similar companies to query company"""
        if not self.is_trained or self.index is None:
            return []
        
        # Convert query company to vector
        query_vector = self.vectorizer.company_to_vector(query_company)
        query_vector = self.vectorizer.transform_vectors(query_vector.reshape(1, -1))
        
        # Search for similar companies
        distances, indices = self.index.search(query_vector.astype(np.float32), k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.companies):
                company = self.companies[idx]
                similarity_score = 1 / (1 + distance)  # Convert distance to similarity
                results.append((company, similarity_score))
        
        return results
    
    def search_by_criteria(self, 
                          stage: str = None,
                          industry: str = None,
                          min_arr: float = None,
                          max_arr: float = None,
                          min_employee_count: int = None,
                          max_employee_count: int = None) -> List[Company]:
        """Search companies by specific criteria"""
        results = []
        
        for company in self.companies:
            # Stage filter
            if stage and company.stage.value != stage:
                continue
            
            # Industry filter
            if industry and industry.lower() not in company.industry.lower():
                continue
            
            # ARR filter
            if min_arr and (company.arr is None or company.arr < min_arr):
                continue
            if max_arr and (company.arr is None or company.arr > max_arr):
                continue
            
            # Employee count filter
            if min_employee_count and (company.employee_count is None or company.employee_count < min_employee_count):
                continue
            if max_employee_count and (company.employee_count is None or company.employee_count > max_employee_count):
                continue
            
            results.append(company)
        
        return results
    
    def get_industry_benchmarks(self, industry: str) -> Dict[str, float]:
        """Calculate industry benchmarks from database"""
        industry_companies = [c for c in self.companies if industry.lower() in c.industry.lower()]
        
        if not industry_companies:
            return {}
        
        metrics = {
            'arr': [c.arr for c in industry_companies if c.arr is not None],
            'cac': [c.cac for c in industry_companies if c.cac is not None],
            'ltv': [c.ltv for c in industry_companies if c.ltv is not None],
            'churn_rate': [c.churn_rate for c in industry_companies if c.churn_rate is not None],
            'growth_rate': [c.growth_rate for c in industry_companies if c.growth_rate is not None],
            'ltv_cac_ratio': [c.ltv_cac_ratio for c in industry_companies if c.ltv_cac_ratio is not None]
        }
        
        benchmarks = {}
        for metric, values in metrics.items():
            if values:
                benchmarks[f'{metric}_median'] = np.median(values)
                benchmarks[f'{metric}_mean'] = np.mean(values)
                benchmarks[f'{metric}_p25'] = np.percentile(values, 25)
                benchmarks[f'{metric}_p75'] = np.percentile(values, 75)
        
        return benchmarks
    
    def save_index(self, filepath: str):
        """Save the FAISS index and metadata"""
        if self.index is not None:
            faiss.write_index(self.index, f"{filepath}.index")
            
            # Save companies and vectorizer
            with open(f"{filepath}_companies.pkl", "wb") as f:
                pickle.dump(self.companies, f)
            
            with open(f"{filepath}_vectorizer.pkl", "wb") as f:
                pickle.dump(self.vectorizer, f)
    
    def load_index(self, filepath: str):
        """Load the FAISS index and metadata"""
        try:
            self.index = faiss.read_index(f"{filepath}.index")
            
            with open(f"{filepath}_companies.pkl", "rb") as f:
                self.companies = pickle.load(f)
            
            with open(f"{filepath}_vectorizer.pkl", "rb") as f:
                self.vectorizer = pickle.load(f)
            
            self.is_trained = True
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the database"""
        if not self.companies:
            return {"total_companies": 0}
        
        stages = {}
        industries = {}
        
        for company in self.companies:
            # Count stages
            stage = company.stage.value
            stages[stage] = stages.get(stage, 0) + 1
            
            # Count industries
            industry = company.industry
            industries[industry] = industries.get(industry, 0) + 1
        
        return {
            "total_companies": len(self.companies),
            "stages": stages,
            "industries": industries,
            "index_size": self.index.ntotal if self.index else 0
        }
