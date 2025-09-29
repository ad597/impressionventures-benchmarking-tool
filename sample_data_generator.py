import random
import numpy as np
from typing import List
from models import Company, CompanyStage

def generate_sample_companies(num_companies: int = 50) -> List[Company]:
    """Generate sample companies for demo purposes"""
    companies = []
    
    industries = ["Payments", "Lending", "Wealth Management", "Insurance", "Banking", "Crypto/DeFi"]
    stages = [CompanyStage.SEED, CompanyStage.SERIES_A, CompanyStage.SERIES_B, CompanyStage.SERIES_C]
    locations = ["San Francisco, CA", "New York, NY", "Toronto, ON", "Austin, TX", "Boston, MA", "Seattle, WA"]
    
    # Industry-specific parameters
    industry_params = {
        "Payments": {
            "arr_range": (100000, 10000000),
            "cac_range": (50, 300),
            "ltv_range": (1000, 8000),
            "churn_range": (0.01, 0.05),
            "growth_range": (0.08, 0.25)
        },
        "Lending": {
            "arr_range": (500000, 15000000),
            "cac_range": (100, 500),
            "ltv_range": (2000, 15000),
            "churn_range": (0.005, 0.03),
            "growth_range": (0.10, 0.30)
        },
        "Wealth Management": {
            "arr_range": (1000000, 20000000),
            "cac_range": (300, 1000),
            "ltv_range": (5000, 50000),
            "churn_range": (0.002, 0.01),
            "growth_range": (0.05, 0.15)
        },
        "Insurance": {
            "arr_range": (200000, 8000000),
            "cac_range": (200, 800),
            "ltv_range": (3000, 20000),
            "churn_range": (0.01, 0.04),
            "growth_range": (0.06, 0.20)
        },
        "Banking": {
            "arr_range": (500000, 25000000),
            "cac_range": (150, 600),
            "ltv_range": (2000, 25000),
            "churn_range": (0.005, 0.02),
            "growth_range": (0.08, 0.18)
        },
        "Crypto/DeFi": {
            "arr_range": (100000, 5000000),
            "cac_range": (100, 400),
            "ltv_range": (1500, 10000),
            "churn_range": (0.02, 0.08),
            "growth_range": (0.10, 0.40)
        }
    }
    
    for i in range(num_companies):
        industry = random.choice(industries)
        stage = random.choice(stages)
        location = random.choice(locations)
        
        # Get industry-specific parameters
        params = industry_params[industry]
        
        # Generate metrics based on industry and stage
        arr = random.uniform(*params["arr_range"])
        cac = random.uniform(*params["cac_range"])
        ltv = random.uniform(*params["ltv_range"])
        churn_rate = random.uniform(*params["churn_range"])
        growth_rate = random.uniform(*params["growth_range"])
        
        # Adjust based on stage
        stage_multipliers = {
            CompanyStage.SEED: 0.3,
            CompanyStage.SERIES_A: 0.6,
            CompanyStage.SERIES_B: 1.0,
            CompanyStage.SERIES_C: 1.5
        }
        
        arr *= stage_multipliers[stage]
        ltv *= stage_multipliers[stage]
        
        # Calculate derived metrics
        ltv_cac_ratio = ltv / cac if cac > 0 else 0
        revenue = arr * random.uniform(0.8, 1.2)  # Revenue close to ARR
        funding_raised = arr * random.uniform(2, 8)  # Funding 2-8x ARR
        valuation = funding_raised * random.uniform(3, 10)  # Valuation 3-10x funding
        
        # Team size based on stage and ARR
        employee_count = int(arr / 50000) + random.randint(5, 20)  # Roughly 1 employee per $50k ARR
        founders_count = random.randint(1, 4)
        
        # Company name generation
        company_names = [
            "PayFlow", "LendTech", "WealthAI", "InsureTech", "BankFlow", "CryptoPay",
            "FinTech Pro", "MoneyFlow", "InvestAI", "LoanFlow", "PayTech", "WealthFlow",
            "InsureFlow", "BankTech", "CryptoFlow", "FinFlow", "MoneyAI", "InvestFlow",
            "LoanAI", "PayAI", "WealthTech", "InsureAI", "BankAI", "CryptoTech"
        ]
        
        name = random.choice(company_names) + f" {random.randint(1, 999)}"
        
        # Business model based on industry
        business_models = {
            "Payments": ["SaaS", "Transaction-based", "Freemium"],
            "Lending": ["Marketplace", "Direct lending", "P2P"],
            "Wealth Management": ["AUM-based", "Subscription", "Commission"],
            "Insurance": ["Commission", "Subscription", "Direct"],
            "Banking": ["Transaction fees", "Interest spread", "Subscription"],
            "Crypto/DeFi": ["Token-based", "Trading fees", "Staking"]
        }
        
        business_model = random.choice(business_models[industry])
        
        # Competitive advantages
        advantages = [
            "AI-powered", "Low fees", "Fast processing", "Easy integration",
            "Advanced analytics", "Mobile-first", "API-first", "Real-time",
            "Automated", "Scalable", "Secure", "User-friendly"
        ]
        
        competitive_advantages = random.sample(advantages, random.randint(2, 4))
        
        # Description
        descriptions = {
            "Payments": f"AI-powered payment processing platform for {random.choice(['SMBs', 'enterprises', 'marketplaces'])}",
            "Lending": f"Digital lending platform for {random.choice(['small businesses', 'consumers', 'real estate'])}",
            "Wealth Management": f"AI-powered wealth management platform for {random.choice(['individuals', 'advisors', 'institutions'])}",
            "Insurance": f"Digital insurance platform for {random.choice(['SMBs', 'individuals', 'enterprises'])}",
            "Banking": f"Digital banking platform for {random.choice(['SMBs', 'consumers', 'enterprises'])}",
            "Crypto/DeFi": f"Crypto and DeFi platform for {random.choice(['trading', 'lending', 'yield farming'])}"
        }
        
        description = descriptions[industry]
        
        # Founded year based on stage
        current_year = 2024
        founded_years = {
            CompanyStage.SEED: random.randint(2022, 2024),
            CompanyStage.SERIES_A: random.randint(2020, 2023),
            CompanyStage.SERIES_B: random.randint(2019, 2022),
            CompanyStage.SERIES_C: random.randint(2018, 2021)
        }
        
        founded_year = founded_years[stage]
        
        company = Company(
            name=name,
            domain=f"{name.lower().replace(' ', '')}.com",
            stage=stage,
            industry=industry,
            founded_year=founded_year,
            location=location,
            arr=arr,
            revenue=revenue,
            funding_raised=funding_raised,
            valuation=valuation,
            cac=cac,
            ltv=ltv,
            ltv_cac_ratio=ltv_cac_ratio,
            churn_rate=churn_rate,
            growth_rate=growth_rate,
            employee_count=employee_count,
            founders_count=founders_count,
            description=description,
            business_model=business_model,
            target_market=random.choice(["SMBs", "Enterprise", "Consumers", "Developers"]),
            competitive_advantages=competitive_advantages,
            data_sources=["sample_data"],
            confidence_score=random.uniform(0.7, 0.95)
        )
        
        companies.append(company)
    
    return companies

def save_sample_data(companies: List[Company], filename: str = "sample_companies.json"):
    """Save sample companies to JSON file"""
    import json
    from datetime import datetime
    
    data = []
    for company in companies:
        company_dict = company.dict()
        # Convert datetime to string for JSON serialization
        company_dict['last_updated'] = company_dict['last_updated'].isoformat()
        data.append(company_dict)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved {len(companies)} companies to {filename}")

def load_sample_data(filename: str = "sample_companies.json") -> List[Company]:
    """Load sample companies from JSON file"""
    import json
    from datetime import datetime
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    companies = []
    for company_dict in data:
        # Convert string back to datetime
        company_dict['last_updated'] = datetime.fromisoformat(company_dict['last_updated'])
        companies.append(Company(**company_dict))
    
    return companies

if __name__ == "__main__":
    # Generate and save sample data
    print("Generating sample companies...")
    companies = generate_sample_companies(100)
    save_sample_data(companies)
    print(f"Generated {len(companies)} sample companies")
    
    # Print some statistics
    industries = {}
    stages = {}
    
    for company in companies:
        industries[company.industry] = industries.get(company.industry, 0) + 1
        stages[company.stage.value] = stages.get(company.stage.value, 0) + 1
    
    print("\nIndustry distribution:")
    for industry, count in industries.items():
        print(f"  {industry}: {count}")
    
    print("\nStage distribution:")
    for stage, count in stages.items():
        print(f"  {stage}: {count}")
