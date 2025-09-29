import json
import re
from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from langchain.chains import LLMChain
from models import Company, ExtractionResult, CompanyStage
from config import Config

class CompanyDataParser(BaseOutputParser):
    """Custom parser for company data extraction"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback to text parsing
                return self._parse_text(text)
        except json.JSONDecodeError:
            return self._parse_text(text)
    
    def _parse_text(self, text: str) -> Dict[str, Any]:
        """Fallback text parsing when JSON extraction fails"""
        data = {}
        lines = text.split('\n')
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                
                # Type conversion
                if key in ['arr', 'revenue', 'funding_raised', 'valuation', 'cac', 'ltv', 'churn_rate', 'growth_rate']:
                    try:
                        data[key] = float(re.sub(r'[^\d.]', '', value))
                    except ValueError:
                        data[key] = None
                elif key in ['founded_year', 'employee_count', 'founders_count']:
                    try:
                        data[key] = int(re.sub(r'[^\d]', '', value))
                    except ValueError:
                        data[key] = None
                else:
                    data[key] = value
        
        return data

class CompanyExtractor:
    """Main class for extracting company data using LLMs"""
    
    def __init__(self):
        # Initialize with mock LLM if no API key is available
        if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != "your_openai_api_key_here":
            self.llm = ChatOpenAI(
                model=Config.DEFAULT_MODEL,
                openai_api_key=Config.OPENAI_API_KEY,
                temperature=0.1
            )
        else:
            self.llm = None  # Will use mock responses
        self.parser = CompanyDataParser()
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Setup extraction prompts for different data sources"""
        
        # Pitch deck extraction prompt
        self.pitch_deck_prompt = PromptTemplate(
            input_variables=["deck_content"],
            template="""
            Extract key company metrics from this pitch deck content. Focus on financial and growth metrics.
            
            Deck Content:
            {deck_content}
            
            Extract the following information in JSON format:
            {{
                "name": "Company name",
                "stage": "seed/series_a/series_b/series_c/series_d/late_stage",
                "industry": "Primary industry",
                "founded_year": year,
                "location": "City, Country",
                "arr": annual_recurring_revenue,
                "revenue": total_revenue,
                "funding_raised": total_funding_raised,
                "valuation": current_valuation,
                "cac": customer_acquisition_cost,
                "ltv": lifetime_value,
                "ltv_cac_ratio": ltv_cac_ratio,
                "churn_rate": monthly_churn_rate,
                "growth_rate": monthly_growth_rate,
                "employee_count": number_of_employees,
                "founders_count": number_of_founders,
                "description": "Company description",
                "business_model": "Business model description",
                "target_market": "Target market description",
                "competitive_advantages": ["advantage1", "advantage2"]
            }}
            
            If any information is not available, use null. Be precise with numbers and conservative with estimates.
            """
        )
        
        # Website extraction prompt
        self.website_prompt = PromptTemplate(
            input_variables=["website_content"],
            template="""
            Extract company information from this website content. Focus on publicly available information.
            
            Website Content:
            {website_content}
            
            Extract the following information in JSON format:
            {{
                "name": "Company name",
                "industry": "Primary industry",
                "founded_year": year,
                "location": "City, Country",
                "description": "Company description",
                "business_model": "Business model description",
                "target_market": "Target market description",
                "competitive_advantages": ["advantage1", "advantage2"]
            }}
            
            If any information is not available, use null. Focus on factual, publicly available information.
            """
        )
        
        # SEC filing extraction prompt
        self.filing_prompt = PromptTemplate(
            input_variables=["filing_content"],
            template="""
            Extract financial and business metrics from this SEC filing content.
            
            Filing Content:
            {filing_content}
            
            Extract the following information in JSON format:
            {{
                "name": "Company name",
                "industry": "Primary industry",
                "revenue": total_revenue,
                "employee_count": number_of_employees,
                "description": "Business description",
                "business_model": "Business model description",
                "target_market": "Target market description"
            }}
            
            Focus on financial data and business model information. Use null for unavailable data.
            """
        )
    
    def extract_from_pitch_deck(self, deck_content: str) -> ExtractionResult:
        """Extract company data from pitch deck content"""
        if self.llm is None:
            # Use mock extraction for demo
            return self._mock_extraction(deck_content, "pitch deck")
        
        chain = LLMChain(llm=self.llm, prompt=self.pitch_deck_prompt, output_parser=self.parser)
        
        try:
            result = chain.run(deck_content=deck_content)
            company_data = self._create_company_from_dict(result)
            
            # Calculate confidence based on data completeness
            confidence = self._calculate_confidence(result)
            missing_fields = self._identify_missing_fields(result)
            
            return ExtractionResult(
                company_data=company_data,
                extraction_confidence=confidence,
                missing_fields=missing_fields,
                extraction_notes="Extracted from pitch deck"
            )
        except Exception as e:
            return ExtractionResult(
                company_data=Company(name="Unknown", stage=CompanyStage.SEED, industry="Unknown"),
                extraction_confidence=0.0,
                missing_fields=[],
                extraction_notes=f"Extraction failed: {str(e)}"
            )
    
    def extract_from_website(self, website_content: str) -> ExtractionResult:
        """Extract company data from website content"""
        if self.llm is None:
            # Use mock extraction for demo
            return self._mock_extraction(website_content, "website")
        
        chain = LLMChain(llm=self.llm, prompt=self.website_prompt, output_parser=self.parser)
        
        try:
            result = chain.run(website_content=website_content)
            company_data = self._create_company_from_dict(result)
            
            confidence = self._calculate_confidence(result)
            missing_fields = self._identify_missing_fields(result)
            
            return ExtractionResult(
                company_data=company_data,
                extraction_confidence=confidence,
                missing_fields=missing_fields,
                extraction_notes="Extracted from website"
            )
        except Exception as e:
            return ExtractionResult(
                company_data=Company(name="Unknown", stage=CompanyStage.SEED, industry="Unknown"),
                extraction_confidence=0.0,
                missing_fields=[],
                extraction_notes=f"Extraction failed: {str(e)}"
            )
    
    def extract_from_filing(self, filing_content: str) -> ExtractionResult:
        """Extract company data from SEC filing content"""
        if self.llm is None:
            # Use mock extraction for demo
            return self._mock_extraction(filing_content, "SEC filing")
        
        chain = LLMChain(llm=self.llm, prompt=self.filing_prompt, output_parser=self.parser)
        
        try:
            result = chain.run(filing_content=filing_content)
            company_data = self._create_company_from_dict(result)
            
            confidence = self._calculate_confidence(result)
            missing_fields = self._identify_missing_fields(result)
            
            return ExtractionResult(
                company_data=company_data,
                extraction_confidence=confidence,
                missing_fields=missing_fields,
                extraction_notes="Extracted from SEC filing"
            )
        except Exception as e:
            return ExtractionResult(
                company_data=Company(name="Unknown", stage=CompanyStage.SEED, industry="Unknown"),
                extraction_confidence=0.0,
                missing_fields=[],
                extraction_notes=f"Extraction failed: {str(e)}"
            )
    
    def _create_company_from_dict(self, data: Dict[str, Any]) -> Company:
        """Create Company object from extracted dictionary"""
        # Map stage string to enum
        stage_mapping = {
            "seed": CompanyStage.SEED,
            "series_a": CompanyStage.SERIES_A,
            "series_b": CompanyStage.SERIES_B,
            "series_c": CompanyStage.SERIES_C,
            "series_d": CompanyStage.SERIES_D,
            "late_stage": CompanyStage.LATE_STAGE
        }
        
        stage = stage_mapping.get(data.get("stage", "seed"), CompanyStage.SEED)
        
        return Company(
            name=data.get("name", "Unknown"),
            domain=data.get("domain"),
            stage=stage,
            industry=data.get("industry", "Unknown"),
            founded_year=data.get("founded_year"),
            location=data.get("location"),
            arr=data.get("arr"),
            revenue=data.get("revenue"),
            funding_raised=data.get("funding_raised"),
            valuation=data.get("valuation"),
            cac=data.get("cac"),
            ltv=data.get("ltv"),
            ltv_cac_ratio=data.get("ltv_cac_ratio"),
            churn_rate=data.get("churn_rate"),
            growth_rate=data.get("growth_rate"),
            employee_count=data.get("employee_count"),
            founders_count=data.get("founders_count"),
            description=data.get("description"),
            business_model=data.get("business_model"),
            target_market=data.get("target_market"),
            competitive_advantages=data.get("competitive_advantages", []),
            data_sources=["llm_extraction"]
        )
    
    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate extraction confidence based on data completeness"""
        required_fields = ["name", "industry", "stage"]
        optional_fields = ["arr", "revenue", "cac", "ltv", "churn_rate", "growth_rate"]
        
        required_score = sum(1 for field in required_fields if data.get(field) is not None) / len(required_fields)
        optional_score = sum(1 for field in optional_fields if data.get(field) is not None) / len(optional_fields)
        
        return (required_score * 0.7) + (optional_score * 0.3)
    
    def _identify_missing_fields(self, data: Dict[str, Any]) -> List[str]:
        """Identify missing important fields"""
        important_fields = ["arr", "cac", "ltv", "churn_rate", "growth_rate", "funding_raised"]
        return [field for field in important_fields if data.get(field) is None]
    
    def _mock_extraction(self, content: str, source_type: str) -> ExtractionResult:
        """Mock extraction for demo purposes when no API key is available"""
        # Simple keyword-based extraction for demo
        content_lower = content.lower()
        
        # Extract basic information
        name = "Demo Company"
        if "payflow" in content_lower or "pay" in content_lower:
            name = "PayFlow"
        elif "lend" in content_lower:
            name = "LendTech"
        elif "wealth" in content_lower:
            name = "WealthAI"
        
        # Mock financial data
        arr = 2500000 if "arr" in content_lower or "revenue" in content_lower else None
        cac = 150 if "cac" in content_lower else None
        ltv = 3000 if "ltv" in content_lower else None
        churn_rate = 0.02 if "churn" in content_lower else None
        growth_rate = 0.15 if "growth" in content_lower else None
        
        # Create company object
        company_data = Company(
            name=name,
            stage=CompanyStage.SERIES_A,
            industry="Payments",
            arr=arr,
            cac=cac,
            ltv=ltv,
            ltv_cac_ratio=ltv/cac if ltv and cac else None,
            churn_rate=churn_rate,
            growth_rate=growth_rate,
            employee_count=45,
            founders_count=2,
            description="Demo company for benchmarking tool",
            data_sources=["mock_extraction"]
        )
        
        return ExtractionResult(
            company_data=company_data,
            extraction_confidence=0.8,  # High confidence for demo
            missing_fields=[],
            extraction_notes=f"Mock extraction from {source_type} (no API key provided)"
        )
