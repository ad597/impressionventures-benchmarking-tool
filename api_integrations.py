import requests
import json
from typing import Dict, Any, Optional, List
from models import Company, CompanyStage
from config import Config

class CrunchbaseAPI:
    """Integration with Crunchbase API for company data"""
    
    def __init__(self):
        self.api_key = Config.CRUNCHBASE_API_KEY
        self.base_url = "https://api.crunchbase.com/v4"
        self.headers = {
            "X-cb-user-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def search_company(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Search for company in Crunchbase"""
        if not self.api_key:
            return self._get_mock_data(company_name)
        
        try:
            url = f"{self.base_url}/searches/organizations"
            params = {
                "query": company_name,
                "limit": 1
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("entities"):
                return data["entities"][0]
            return None
            
        except Exception as e:
            print(f"Crunchbase API error: {e}")
            return self._get_mock_data(company_name)
    
    def get_company_details(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed company information"""
        if not self.api_key:
            return self._get_mock_company_details()
        
        try:
            url = f"{self.base_url}/entities/organizations/{entity_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Crunchbase API error: {e}")
            return self._get_mock_company_details()
    
    def _get_mock_data(self, company_name: str) -> Dict[str, Any]:
        """Mock data for demo purposes"""
        return {
            "uuid": f"mock-{company_name.lower().replace(' ', '-')}",
            "properties": {
                "name": company_name,
                "short_description": f"Mock description for {company_name}",
                "category_list": ["Financial Services", "Technology"],
                "founded_on": "2020-01-01",
                "num_employees_enum": "11-50"
            }
        }
    
    def _get_mock_company_details(self) -> Dict[str, Any]:
        """Mock detailed company data"""
        return {
            "properties": {
                "name": "Mock Company",
                "short_description": "Mock fintech company",
                "category_list": ["Financial Services"],
                "founded_on": "2020-01-01",
                "num_employees_enum": "11-50",
                "total_funding_usd": 5000000,
                "last_funding_round_type": "Series A"
            }
        }

class LinkedInAPI:
    """Integration with LinkedIn API for company data"""
    
    def __init__(self):
        self.api_key = Config.LINKEDIN_API_KEY
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def search_company(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Search for company on LinkedIn"""
        if not self.api_key:
            return self._get_mock_linkedin_data(company_name)
        
        try:
            url = f"{self.base_url}/organizationSearch"
            params = {
                "q": company_name,
                "count": 1
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("elements"):
                return data["elements"][0]
            return None
            
        except Exception as e:
            print(f"LinkedIn API error: {e}")
            return self._get_mock_linkedin_data(company_name)
    
    def _get_mock_linkedin_data(self, company_name: str) -> Dict[str, Any]:
        """Mock LinkedIn data for demo"""
        return {
            "id": f"mock-linkedin-{company_name.lower().replace(' ', '-')}",
            "name": company_name,
            "description": f"Mock LinkedIn description for {company_name}",
            "industry": "Financial Services",
            "employeeCountRange": "11-50"
        }

class FintechDataProvider:
    """Mock fintech data provider for specialized metrics"""
    
    def __init__(self):
        self.data_cache = {}
    
    def get_fintech_metrics(self, company_name: str, industry: str) -> Dict[str, Any]:
        """Get fintech-specific metrics"""
        # Mock data based on industry
        if "payment" in industry.lower():
            return {
                "transaction_volume": 1000000,
                "merchant_count": 5000,
                "payment_methods": ["credit_card", "debit_card", "bank_transfer"],
                "geographic_reach": ["US", "Canada"],
                "compliance_score": 0.85
            }
        elif "lending" in industry.lower():
            return {
                "loan_volume": 50000000,
                "borrower_count": 10000,
                "default_rate": 0.03,
                "interest_rate_range": [0.05, 0.15],
                "regulatory_status": "licensed"
            }
        elif "wealth" in industry.lower() or "investment" in industry.lower():
            return {
                "aum": 100000000,  # Assets under management
                "client_count": 2000,
                "average_account_size": 50000,
                "investment_products": ["ETFs", "Mutual Funds", "Stocks"],
                "fiduciary_status": "fiduciary"
            }
        else:
            return {
                "user_count": 50000,
                "monthly_active_users": 40000,
                "retention_rate": 0.85,
                "feature_adoption": 0.70
            }
    
    def get_industry_benchmarks(self, industry: str) -> Dict[str, Any]:
        """Get industry-specific benchmarks"""
        benchmarks = {
            "payments": {
                "avg_cac": 150,
                "avg_ltv": 2000,
                "avg_churn": 0.02,
                "avg_growth_rate": 0.15
            },
            "lending": {
                "avg_cac": 200,
                "avg_ltv": 5000,
                "avg_churn": 0.01,
                "avg_growth_rate": 0.20
            },
            "wealth_management": {
                "avg_cac": 500,
                "avg_ltv": 15000,
                "avg_churn": 0.005,
                "avg_growth_rate": 0.10
            },
            "insurance": {
                "avg_cac": 300,
                "avg_ltv": 8000,
                "avg_churn": 0.03,
                "avg_growth_rate": 0.12
            }
        }
        
        return benchmarks.get(industry.lower(), {
            "avg_cac": 250,
            "avg_ltv": 4000,
            "avg_churn": 0.02,
            "avg_growth_rate": 0.15
        })

class DataAggregator:
    """Main class for aggregating data from multiple sources"""
    
    def __init__(self):
        self.crunchbase = CrunchbaseAPI()
        self.linkedin = LinkedInAPI()
        self.fintech_provider = FintechDataProvider()
    
    def enrich_company_data(self, company: Company) -> Company:
        """Enrich company data with external sources"""
        # Get data from Crunchbase
        cb_data = self.crunchbase.search_company(company.name)
        if cb_data:
            company = self._merge_crunchbase_data(company, cb_data)
        
        # Get data from LinkedIn
        linkedin_data = self.linkedin.search_company(company.name)
        if linkedin_data:
            company = self._merge_linkedin_data(company, linkedin_data)
        
        # Get fintech-specific metrics
        fintech_metrics = self.fintech_provider.get_fintech_metrics(
            company.name, company.industry
        )
        company = self._merge_fintech_data(company, fintech_metrics)
        
        # Add data sources
        company.data_sources.extend(["crunchbase", "linkedin", "fintech_provider"])
        
        return company
    
    def _merge_crunchbase_data(self, company: Company, cb_data: Dict[str, Any]) -> Company:
        """Merge Crunchbase data into company object"""
        properties = cb_data.get("properties", {})
        
        if not company.founded_year and properties.get("founded_on"):
            try:
                company.founded_year = int(properties["founded_on"][:4])
            except:
                pass
        
        if not company.employee_count and properties.get("num_employees_enum"):
            employee_mapping = {
                "1-10": 5,
                "11-50": 30,
                "51-200": 125,
                "201-500": 350,
                "501-1000": 750,
                "1001-5000": 3000,
                "5001-10000": 7500,
                "10001+": 15000
            }
            company.employee_count = employee_mapping.get(properties["num_employees_enum"])
        
        if not company.funding_raised and properties.get("total_funding_usd"):
            company.funding_raised = properties["total_funding_usd"]
        
        return company
    
    def _merge_linkedin_data(self, company: Company, linkedin_data: Dict[str, Any]) -> Company:
        """Merge LinkedIn data into company object"""
        if not company.description and linkedin_data.get("description"):
            company.description = linkedin_data["description"]
        
        if not company.employee_count and linkedin_data.get("employeeCountRange"):
            employee_mapping = {
                "1-10": 5,
                "11-50": 30,
                "51-200": 125,
                "201-500": 350,
                "501-1000": 750,
                "1001-5000": 3000,
                "5001-10000": 7500,
                "10001+": 15000
            }
            company.employee_count = employee_mapping.get(linkedin_data["employeeCountRange"])
        
        return company
    
    def _merge_fintech_data(self, company: Company, fintech_data: Dict[str, Any]) -> Company:
        """Merge fintech-specific data into company object"""
        # Store fintech-specific metrics in a custom field
        if not hasattr(company, 'fintech_metrics'):
            company.fintech_metrics = fintech_data
        
        return company
