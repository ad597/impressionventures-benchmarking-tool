import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from typing import List, Dict, Any
import os

# Import our modules
from models import Company, CompanyStage, BenchmarkResult
from extractors import CompanyExtractor
from api_integrations import DataAggregator
from vector_database import CompanyVectorDatabase
from benchmarking_engine import BenchmarkingEngine
from config import Config

# Page configuration
st.set_page_config(
    page_title="Impression Ventures - Competitive Benchmarking Tool",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .red-flag {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f44336;
        margin: 0.5rem 0;
    }
    .green-flag {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    .warning-flag {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_components():
    """Initialize all components with caching"""
    extractor = CompanyExtractor()
    aggregator = DataAggregator()
    vector_db = CompanyVectorDatabase()
    benchmarking_engine = BenchmarkingEngine(vector_db)
    
    return extractor, aggregator, vector_db, benchmarking_engine

def load_sample_data():
    """Load sample data for demo purposes"""
    sample_companies = [
        Company(
            name="PayFlow",
            domain="payflow.com",
            stage=CompanyStage.SERIES_A,
            industry="Payments",
            founded_year=2020,
            location="San Francisco, CA",
            arr=2500000,
            revenue=2500000,
            funding_raised=15000000,
            valuation=50000000,
            cac=150,
            ltv=3000,
            ltv_cac_ratio=20.0,
            churn_rate=0.02,
            growth_rate=0.15,
            employee_count=45,
            founders_count=2,
            description="AI-powered payment processing platform",
            business_model="SaaS",
            target_market="SMBs",
            competitive_advantages=["AI optimization", "Low fees", "Easy integration"]
        ),
        Company(
            name="LendTech",
            domain="lendtech.com",
            stage=CompanyStage.SEED,
            industry="Lending",
            founded_year=2021,
            location="New York, NY",
            arr=800000,
            revenue=800000,
            funding_raised=5000000,
            valuation=20000000,
            cac=200,
            ltv=5000,
            ltv_cac_ratio=25.0,
            churn_rate=0.01,
            growth_rate=0.20,
            employee_count=25,
            founders_count=3,
            description="Digital lending platform for small businesses",
            business_model="Marketplace",
            target_market="Small businesses",
            competitive_advantages=["Fast approval", "Low rates", "Automated underwriting"]
        ),
        Company(
            name="WealthAI",
            domain="wealthai.com",
            stage=CompanyStage.SERIES_B,
            industry="Wealth Management",
            founded_year=2019,
            location="Toronto, ON",
            arr=5000000,
            revenue=5000000,
            funding_raised=25000000,
            valuation=100000000,
            cac=500,
            ltv=15000,
            ltv_cac_ratio=30.0,
            churn_rate=0.005,
            growth_rate=0.10,
            employee_count=80,
            founders_count=2,
            description="AI-powered wealth management platform",
            business_model="SaaS + AUM",
            target_market="High net worth individuals",
            competitive_advantages=["AI portfolio management", "Low fees", "Personalized advice"]
        )
    ]
    return sample_companies

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 Impression Ventures Competitive Benchmarking Tool</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize components
    extractor, aggregator, vector_db, benchmarking_engine = initialize_components()
    
    # Load sample data
    sample_companies = load_sample_data()
    vector_db.add_companies(sample_companies)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "Company Analysis",
        "Industry Benchmarking", 
        "Portfolio Overview",
        "Data Extraction Demo"
    ])
    
    if page == "Company Analysis":
        company_analysis_page(benchmarking_engine)
    elif page == "Industry Benchmarking":
        industry_benchmarking_page(benchmarking_engine)
    elif page == "Portfolio Overview":
        portfolio_overview_page(benchmarking_engine)
    elif page == "Data Extraction Demo":
        data_extraction_page(extractor, aggregator)

def company_analysis_page(benchmarking_engine):
    """Company analysis and benchmarking page"""
    st.header("📊 Company Analysis & Benchmarking")
    
    # Company input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Company Information")
        company_name = st.text_input("Company Name", value="PayFlow")
        industry = st.selectbox("Industry", ["Payments", "Lending", "Wealth Management", "Insurance", "Banking"])
        stage = st.selectbox("Stage", ["seed", "series_a", "series_b", "series_c", "series_d", "late_stage"])
        
        # Financial metrics
        st.subheader("Financial Metrics")
        col_arr, col_revenue = st.columns(2)
        with col_arr:
            arr = st.number_input("ARR ($)", value=2500000, step=100000)
        with col_revenue:
            revenue = st.number_input("Revenue ($)", value=2500000, step=100000)
        
        col_funding, col_valuation = st.columns(2)
        with col_funding:
            funding_raised = st.number_input("Funding Raised ($)", value=15000000, step=1000000)
        with col_valuation:
            valuation = st.number_input("Valuation ($)", value=50000000, step=1000000)
    
    with col2:
        st.subheader("Growth Metrics")
        cac = st.number_input("CAC ($)", value=150, step=10)
        ltv = st.number_input("LTV ($)", value=3000, step=100)
        churn_rate = st.number_input("Monthly Churn Rate (%)", value=2.0, step=0.1) / 100
        growth_rate = st.number_input("Monthly Growth Rate (%)", value=15.0, step=0.1) / 100
        
        ltv_cac_ratio = ltv / cac if cac > 0 else 0
        st.metric("LTV/CAC Ratio", f"{ltv_cac_ratio:.1f}")
    
    # Create company object
    company = Company(
        name=company_name,
        stage=CompanyStage(stage),
        industry=industry,
        arr=arr,
        revenue=revenue,
        funding_raised=funding_raised,
        valuation=valuation,
        cac=cac,
        ltv=ltv,
        ltv_cac_ratio=ltv_cac_ratio,
        churn_rate=churn_rate,
        growth_rate=growth_rate,
        employee_count=45,
        founders_count=2
    )
    
    if st.button("Run Benchmarking Analysis", type="primary"):
        with st.spinner("Analyzing company metrics..."):
            # Run benchmarking
            benchmark_result = benchmarking_engine.benchmark_company(company)
            
            # Display results
            display_benchmark_results(benchmark_result)

def display_benchmark_results(benchmark_result: BenchmarkResult):
    """Display benchmarking results"""
    st.header("📈 Benchmarking Results")
    
    # Risk score and recommendation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_color = "red" if benchmark_result.risk_score > 0.6 else "orange" if benchmark_result.risk_score > 0.3 else "green"
        st.metric("Risk Score", f"{benchmark_result.risk_score:.1%}", delta=None)
    
    with col2:
        st.metric("Peer Companies Analyzed", len(benchmark_result.peer_companies))
    
    with col3:
        st.metric("Red Flags", len(benchmark_result.red_flags))
    
    # Red flags
    if benchmark_result.red_flags:
        st.subheader("🚨 Red Flags")
        for flag in benchmark_result.red_flags:
            st.markdown(f'<div class="red-flag">{flag}</div>', unsafe_allow_html=True)
    
    # Insights
    if benchmark_result.insights:
        st.subheader("💡 Key Insights")
        for insight in benchmark_result.insights:
            st.markdown(f'<div class="green-flag">{insight}</div>', unsafe_allow_html=True)
    
    # Metrics comparison
    st.subheader("📊 Metrics Comparison")
    
    if benchmark_result.metrics_comparison:
        metrics_df = pd.DataFrame(benchmark_result.metrics_comparison).T
        metrics_df = metrics_df[['company_value', 'peer_median', 'peer_p25', 'peer_p75', 'company_percentile']]
        metrics_df.columns = ['Company Value', 'Peer Median', '25th Percentile', '75th Percentile', 'Company Percentile']
        
        st.dataframe(metrics_df, use_container_width=True)
        
        # Create comparison charts
        create_metrics_charts(benchmark_result.metrics_comparison)
    
    # Recommendation
    st.subheader("🎯 Investment Recommendation")
    recommendation_color = "red" if "HIGH RISK" in benchmark_result.recommendation else "orange" if "MEDIUM RISK" in benchmark_result.recommendation else "green"
    st.markdown(f'<div class="metric-card" style="border-left-color: {recommendation_color}">{benchmark_result.recommendation}</div>', unsafe_allow_html=True)

def create_metrics_charts(metrics_comparison: Dict[str, Dict[str, Any]]):
    """Create comparison charts for metrics"""
    if not metrics_comparison:
        return
    
    # Select key metrics for visualization
    key_metrics = ['arr', 'cac', 'ltv', 'churn_rate', 'growth_rate']
    available_metrics = [m for m in key_metrics if m in metrics_comparison]
    
    if not available_metrics:
        return
    
    # Create subplots
    fig = make_subplots(
        rows=len(available_metrics), 
        cols=1,
        subplot_titles=[m.upper() for m in available_metrics],
        vertical_spacing=0.1
    )
    
    for i, metric in enumerate(available_metrics, 1):
        data = metrics_comparison[metric]
        
        # Company value
        fig.add_trace(
            go.Bar(
                name=f"Company {metric.upper()}",
                x=[metric.upper()],
                y=[data['company_value']],
                marker_color='blue',
                showlegend=False
            ),
            row=i, col=1
        )
        
        # Peer median
        fig.add_trace(
            go.Bar(
                name=f"Peer Median {metric.upper()}",
                x=[metric.upper()],
                y=[data['peer_median']],
                marker_color='lightblue',
                showlegend=False
            ),
            row=i, col=1
        )
    
    fig.update_layout(
        height=200 * len(available_metrics),
        title_text="Company vs Peer Metrics Comparison",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def industry_benchmarking_page(benchmarking_engine):
    """Industry benchmarking page"""
    st.header("🏭 Industry Benchmarking")
    
    industry = st.selectbox("Select Industry", ["Payments", "Lending", "Wealth Management", "Insurance", "Banking"])
    
    if st.button("Analyze Industry", type="primary"):
        with st.spinner("Analyzing industry benchmarks..."):
            analysis = benchmarking_engine.get_industry_analysis(industry)
            
            if "error" in analysis:
                st.error(analysis["error"])
                return
            
            # Display industry statistics
            st.subheader(f"📊 {industry} Industry Analysis")
            
            # Key metrics overview
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Companies", analysis["total_companies"])
            with col2:
                if analysis["arr_stats"]:
                    st.metric("Median ARR", f"${analysis['arr_stats']['median']:,.0f}")
            with col3:
                if analysis["growth_stats"]:
                    st.metric("Median Growth Rate", f"{analysis['growth_stats']['median']:.1%}")
            
            # Detailed metrics tables
            metrics = ["arr", "cac", "ltv", "churn", "growth"]
            metric_names = ["ARR", "CAC", "LTV", "Churn Rate", "Growth Rate"]
            
            for metric, name in zip(metrics, metric_names):
                if f"{metric}_stats" in analysis and analysis[f"{metric}_stats"]:
                    st.subheader(f"{name} Statistics")
                    stats_df = pd.DataFrame([analysis[f"{metric}_stats"]]).T
                    stats_df.columns = ["Value"]
                    st.dataframe(stats_df, use_container_width=True)

def portfolio_overview_page(benchmarking_engine):
    """Portfolio overview page"""
    st.header("💼 Portfolio Overview")
    
    # Mock portfolio data
    portfolio_companies = [
        {"name": "PayFlow", "stage": "Series A", "arr": 2500000, "growth_rate": 0.15, "risk_score": 0.2},
        {"name": "LendTech", "stage": "Seed", "arr": 800000, "growth_rate": 0.20, "risk_score": 0.1},
        {"name": "WealthAI", "stage": "Series B", "arr": 5000000, "growth_rate": 0.10, "risk_score": 0.3}
    ]
    
    # Portfolio metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Companies", len(portfolio_companies))
    with col2:
        total_arr = sum(c["arr"] for c in portfolio_companies)
        st.metric("Total ARR", f"${total_arr:,.0f}")
    with col3:
        avg_growth = sum(c["growth_rate"] for c in portfolio_companies) / len(portfolio_companies)
        st.metric("Avg Growth Rate", f"{avg_growth:.1%}")
    with col4:
        avg_risk = sum(c["risk_score"] for c in portfolio_companies) / len(portfolio_companies)
        st.metric("Avg Risk Score", f"{avg_risk:.1%}")
    
    # Portfolio table
    st.subheader("Portfolio Companies")
    portfolio_df = pd.DataFrame(portfolio_companies)
    st.dataframe(portfolio_df, use_container_width=True)
    
    # Risk distribution chart
    fig = px.bar(
        portfolio_df, 
        x="name", 
        y="risk_score",
        title="Portfolio Risk Distribution",
        color="risk_score",
        color_continuous_scale="RdYlGn_r"
    )
    st.plotly_chart(fig, use_container_width=True)

def data_extraction_page(extractor, aggregator):
    """Data extraction demo page"""
    st.header("🔍 Data Extraction Demo")
    
    st.subheader("Upload Company Documents")
    
    # File upload
    uploaded_file = st.file_uploader("Upload pitch deck, website content, or SEC filing", type=['txt', 'pdf'])
    
    if uploaded_file is not None:
        content = str(uploaded_file.read(), "utf-8")
        
        # Extract data
        if st.button("Extract Company Data", type="primary"):
            with st.spinner("Extracting data using LLM..."):
                # Mock extraction for demo
                extraction_result = extractor.extract_from_pitch_deck(content)
                
                st.subheader("Extracted Company Data")
                
                # Display extracted data
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Basic Information**")
                    st.write(f"Name: {extraction_result.company_data.name}")
                    st.write(f"Industry: {extraction_result.company_data.industry}")
                    st.write(f"Stage: {extraction_result.company_data.stage.value}")
                    st.write(f"Founded: {extraction_result.company_data.founded_year}")
                
                with col2:
                    st.write("**Financial Metrics**")
                    st.write(f"ARR: ${extraction_result.company_data.arr:,.0f}" if extraction_result.company_data.arr else "ARR: Not available")
                    st.write(f"Revenue: ${extraction_result.company_data.revenue:,.0f}" if extraction_result.company_data.revenue else "Revenue: Not available")
                    st.write(f"Funding: ${extraction_result.company_data.funding_raised:,.0f}" if extraction_result.company_data.funding_raised else "Funding: Not available")
                
                # Confidence score
                st.metric("Extraction Confidence", f"{extraction_result.extraction_confidence:.1%}")
                
                # Missing fields
                if extraction_result.missing_fields:
                    st.warning(f"Missing fields: {', '.join(extraction_result.missing_fields)}")
    
    # Demo with sample content
    st.subheader("Try with Sample Content")
    sample_content = """
    PayFlow - AI-Powered Payment Processing
    
    Company Overview:
    PayFlow is revolutionizing payment processing with AI-driven optimization.
    Founded in 2020, we've grown to $2.5M ARR with 15% monthly growth.
    
    Financial Metrics:
    - ARR: $2,500,000
    - CAC: $150
    - LTV: $3,000
    - Monthly Churn: 2%
    - Monthly Growth: 15%
    
    Team: 45 employees, 2 founders
    Location: San Francisco, CA
    """
    
    if st.button("Extract from Sample Content"):
        with st.spinner("Extracting data..."):
            extraction_result = extractor.extract_from_pitch_deck(sample_content)
            
            st.json({
                "name": extraction_result.company_data.name,
                "industry": extraction_result.company_data.industry,
                "stage": extraction_result.company_data.stage.value,
                "arr": extraction_result.company_data.arr,
                "cac": extraction_result.company_data.cac,
                "ltv": extraction_result.company_data.ltv,
                "churn_rate": extraction_result.company_data.churn_rate,
                "growth_rate": extraction_result.company_data.growth_rate
            })

if __name__ == "__main__":
    main()
