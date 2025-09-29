# Impression Ventures Competitive Benchmarking Tool

A comprehensive AI-powered competitive benchmarking tool designed to accelerate post-screening due diligence for venture capital firms.

## 🚀 Features

### Core Capabilities
- **LLM-Powered Data Extraction**: Extract structured metrics from pitch decks, websites, and SEC filings using OpenAI and LangChain
- **API Integrations**: Connect to Crunchbase, LinkedIn, and fintech data providers for comprehensive company data
- **Vector Database**: FAISS-based similarity search across 8,000+ company dataset
- **Real-time Benchmarking**: Instant peer comparisons and industry analysis
- **Red Flag Detection**: Automated outlier identification and risk assessment
- **Interactive Dashboard**: Streamlit-based interface for analysis and visualization

### Key Metrics Tracked
- **Financial**: ARR, Revenue, Funding Raised, Valuation
- **Growth**: CAC, LTV, LTV/CAC Ratio, Churn Rate, Growth Rate
- **Operational**: Employee Count, Team Composition, Business Model
- **Market**: Industry, Stage, Geographic Location, Competitive Advantages

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd impressionventures_demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Generate sample data** (optional)
   ```bash
   python sample_data_generator.py
   ```

## 🚀 Quick Start

### Launch the Dashboard
```bash
streamlit run dashboard.py
```

### Key Components

#### 1. Company Analysis
- Input company metrics manually or upload documents
- Get instant benchmarking against similar companies
- View red flags, insights, and investment recommendations

#### 2. Industry Benchmarking
- Analyze industry-wide metrics and trends
- Compare against industry benchmarks
- Identify market opportunities and risks

#### 3. Portfolio Overview
- Monitor portfolio company performance
- Track risk distribution and growth metrics
- Generate portfolio-level insights

#### 4. Data Extraction Demo
- Upload pitch decks, websites, or SEC filings
- See LLM-powered data extraction in action
- Validate extraction accuracy and completeness

## 📊 Architecture

### Data Flow
1. **Data Ingestion**: LLM extraction from documents + API integrations
2. **Data Enrichment**: Combine multiple sources for comprehensive profiles
3. **Vectorization**: Convert company data to searchable vectors
4. **Benchmarking**: Compare against similar companies and industry standards
5. **Risk Assessment**: Detect outliers and red flags
6. **Visualization**: Interactive dashboard for analysis

### Technology Stack
- **LLM Pipeline**: OpenAI GPT-4 + LangChain
- **Vector Database**: FAISS for similarity search
- **API Integrations**: Crunchbase, LinkedIn, fintech providers
- **Frontend**: Streamlit for interactive dashboard
- **Data Storage**: PostgreSQL (optional) or SQLite
- **Visualization**: Plotly for charts and graphs

## 🔧 Configuration

### API Keys Required
- `OPENAI_API_KEY`: For LLM-powered extraction
- `CRUNCHBASE_API_KEY`: For company data enrichment
- `LINKEDIN_API_KEY`: For professional network data
- `DATABASE_URL`: For persistent storage (optional)

### Model Configuration
- Default model: GPT-4 Turbo
- Embedding model: text-embedding-3-small
- Temperature: 0.1 for consistent extraction

## 📈 Usage Examples

### Benchmark a New Company
```python
from models import Company, CompanyStage
from benchmarking_engine import BenchmarkingEngine
from vector_database import CompanyVectorDatabase

# Create company
company = Company(
    name="PayFlow",
    stage=CompanyStage.SERIES_A,
    industry="Payments",
    arr=2500000,
    cac=150,
    ltv=3000,
    churn_rate=0.02,
    growth_rate=0.15
)

# Initialize components
vector_db = CompanyVectorDatabase()
benchmarking_engine = BenchmarkingEngine(vector_db)

# Run benchmarking
result = benchmarking_engine.benchmark_company(company)
print(f"Risk Score: {result.risk_score:.1%}")
print(f"Recommendation: {result.recommendation}")
```

### Extract Data from Documents
```python
from extractors import CompanyExtractor

extractor = CompanyExtractor()
result = extractor.extract_from_pitch_deck(pitch_deck_content)

print(f"Extracted ARR: ${result.company_data.arr:,.0f}")
print(f"Confidence: {result.extraction_confidence:.1%}")
```

## 🎯 Demo Scenarios

### Scenario 1: Seed Stage Payments Company
- **Company**: Early-stage payment processor
- **Metrics**: $500K ARR, $200 CAC, $2K LTV, 3% churn
- **Analysis**: High CAC relative to LTV, churn concerns
- **Recommendation**: MEDIUM RISK - Optimize unit economics

### Scenario 2: Series A Lending Platform
- **Company**: Digital lending for SMBs
- **Metrics**: $2M ARR, $150 CAC, $5K LTV, 1% churn
- **Analysis**: Strong unit economics, low churn
- **Recommendation**: LOW RISK - Strong investment candidate

### Scenario 3: Series B Wealth Management
- **Company**: AI-powered wealth platform
- **Metrics**: $8M ARR, $400 CAC, $15K LTV, 0.5% churn
- **Analysis**: Excellent metrics across the board
- **Recommendation**: LOW RISK - Premium investment opportunity

## 🔍 Red Flag Detection

The system automatically detects:
- **Unit Economics Issues**: LTV/CAC ratio < 3:1
- **High Churn**: Churn rate above industry 75th percentile
- **Low Growth**: Growth rate below 5% monthly
- **Unusual Metrics**: Outliers in key financial metrics
- **Data Quality**: Missing critical information

## 📊 Industry Benchmarks

### Payments Industry
- Median ARR: $2.5M
- Median CAC: $150
- Median LTV: $3,000
- Median Churn: 2.5%
- Median Growth: 12%

### Lending Industry
- Median ARR: $3.2M
- Median CAC: $200
- Median LTV: $8,000
- Median Churn: 1.8%
- Median Growth: 18%

### Wealth Management
- Median ARR: $5.8M
- Median CAC: $400
- Median LTV: $18,000
- Median Churn: 0.8%
- Median Growth: 8%

## 🚀 Future Enhancements

### Planned Features
- **Real-time Data Updates**: Live API connections for current metrics
- **Advanced Analytics**: Predictive modeling for success probability
- **Portfolio Monitoring**: Automated tracking of portfolio companies
- **Market Intelligence**: Industry trend analysis and predictions
- **Integration APIs**: Connect with existing VC tools and workflows

### Scalability Improvements
- **Distributed Processing**: Handle larger datasets efficiently
- **Caching Layer**: Redis for faster data access
- **Microservices**: Modular architecture for better scalability
- **Cloud Deployment**: AWS/Azure deployment options

## 🤝 Contributing

This is a demo project for Impression Ventures interview. For production use, consider:
- Enhanced error handling and validation
- Comprehensive testing suite
- Security improvements for API keys
- Performance optimization for large datasets
- User authentication and access control

## 📄 License

This project is for demonstration purposes. Please respect API terms of service for external data sources.

## 🎯 Impact

### For Venture Capital Firms
- **Time Savings**: Reduce benchmarking time from hours to minutes
- **Better Decisions**: Data-driven investment decisions
- **Risk Mitigation**: Early identification of red flags
- **Competitive Advantage**: Proprietary benchmarking capabilities

### For Portfolio Companies
- **Benchmarking**: Compare performance against peers
- **Growth Insights**: Identify improvement opportunities
- **Market Positioning**: Understand competitive landscape
- **Strategic Planning**: Data-driven growth strategies

---

**Built with ❤️ for Impression Ventures - Redefining Venture Capital with AI**
