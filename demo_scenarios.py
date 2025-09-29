"""
Demo scenarios for Impression Ventures Competitive Benchmarking Tool
"""

from models import Company, CompanyStage
from vector_database import CompanyVectorDatabase
from benchmarking_engine import BenchmarkingEngine
from sample_data_generator import generate_sample_companies

def demo_scenario_1():
    """Demo Scenario 1: High-Risk Payments Company"""
    print("🎯 DEMO SCENARIO 1: High-Risk Payments Company")
    print("=" * 50)
    
    # Create a high-risk company
    company = Company(
        name="PayFlow",
        stage=CompanyStage.SERIES_A,
        industry="Payments",
        arr=500000,  # Low ARR
        cac=500,     # High CAC
        ltv=1000,    # Low LTV
        ltv_cac_ratio=2.0,  # Poor ratio
        churn_rate=0.08,     # High churn
        growth_rate=0.05,    # Low growth
        employee_count=25,
        founders_count=2
    )
    
    print(f"Company: {company.name}")
    print(f"ARR: ${company.arr:,.0f}")
    print(f"CAC: ${company.cac:,.0f}")
    print(f"LTV: ${company.ltv:,.0f}")
    print(f"LTV/CAC: {company.ltv_cac_ratio:.1f}")
    print(f"Churn: {company.churn_rate:.1%}")
    print(f"Growth: {company.growth_rate:.1%}")
    
    return company

def demo_scenario_2():
    """Demo Scenario 2: Strong Lending Company"""
    print("\n🎯 DEMO SCENARIO 2: Strong Lending Company")
    print("=" * 50)
    
    # Create a strong company
    company = Company(
        name="LendTech",
        stage=CompanyStage.SERIES_A,
        industry="Lending",
        arr=2000000,  # Good ARR
        cac=150,      # Low CAC
        ltv=5000,     # High LTV
        ltv_cac_ratio=33.3,  # Excellent ratio
        churn_rate=0.01,     # Low churn
        growth_rate=0.20,    # High growth
        employee_count=45,
        founders_count=3
    )
    
    print(f"Company: {company.name}")
    print(f"ARR: ${company.arr:,.0f}")
    print(f"CAC: ${company.cac:,.0f}")
    print(f"LTV: ${company.ltv:,.0f}")
    print(f"LTV/CAC: {company.ltv_cac_ratio:.1f}")
    print(f"Churn: {company.churn_rate:.1%}")
    print(f"Growth: {company.growth_rate:.1%}")
    
    return company

def demo_scenario_3():
    """Demo Scenario 3: Premium Wealth Management Company"""
    print("\n🎯 DEMO SCENARIO 3: Premium Wealth Management Company")
    print("=" * 50)
    
    # Create a premium company
    company = Company(
        name="WealthAI",
        stage=CompanyStage.SERIES_B,
        industry="Wealth Management",
        arr=8000000,  # High ARR
        cac=400,      # Moderate CAC
        ltv=20000,    # Very high LTV
        ltv_cac_ratio=50.0,  # Excellent ratio
        churn_rate=0.005,    # Very low churn
        growth_rate=0.12,    # Good growth
        employee_count=80,
        founders_count=2
    )
    
    print(f"Company: {company.name}")
    print(f"ARR: ${company.arr:,.0f}")
    print(f"CAC: ${company.cac:,.0f}")
    print(f"LTV: ${company.ltv:,.0f}")
    print(f"LTV/CAC: {company.ltv_cac_ratio:.1f}")
    print(f"Churn: {company.churn_rate:.1%}")
    print(f"Growth: {company.growth_rate:.1%}")
    
    return company

def run_benchmarking_demo():
    """Run complete benchmarking demo"""
    print("🚀 IMPRESSION VENTURES BENCHMARKING DEMO")
    print("=" * 60)
    
    # Initialize components
    vector_db = CompanyVectorDatabase()
    benchmarking_engine = BenchmarkingEngine(vector_db)
    
    # Generate sample data
    print("📊 Loading sample data...")
    sample_companies = generate_sample_companies(100)
    vector_db.add_companies(sample_companies)
    print(f"✅ Loaded {len(sample_companies)} companies")
    
    # Demo scenarios
    scenarios = [
        ("High-Risk Payments", demo_scenario_1),
        ("Strong Lending", demo_scenario_2),
        ("Premium Wealth Management", demo_scenario_3)
    ]
    
    for scenario_name, scenario_func in scenarios:
        print(f"\n{'='*60}")
        print(f"SCENARIO: {scenario_name}")
        print('='*60)
        
        # Create company
        company = scenario_func()
        
        # Run benchmarking
        print(f"\n🔍 Running benchmarking analysis...")
        result = benchmarking_engine.benchmark_company(company)
        
        # Display results
        print(f"\n📊 BENCHMARKING RESULTS:")
        print(f"Risk Score: {result.risk_score:.1%}")
        print(f"Peer Companies: {len(result.peer_companies)}")
        print(f"Red Flags: {len(result.red_flags)}")
        
        if result.red_flags:
            print(f"\n🚨 RED FLAGS:")
            for flag in result.red_flags:
                print(f"  • {flag}")
        
        if result.insights:
            print(f"\n💡 INSIGHTS:")
            for insight in result.insights:
                print(f"  • {insight}")
        
        print(f"\n🎯 RECOMMENDATION:")
        print(f"  {result.recommendation}")
        
        # Key metrics comparison
        if result.metrics_comparison:
            print(f"\n📈 KEY METRICS COMPARISON:")
            for metric, data in result.metrics_comparison.items():
                if metric in ['arr', 'cac', 'ltv', 'churn_rate', 'growth_rate']:
                    company_val = data['company_value']
                    peer_median = data['peer_median']
                    percentile = data['company_percentile']
                    print(f"  {metric.upper()}: ${company_val:,.0f} vs ${peer_median:,.0f} (peer median) - {percentile:.0f}th percentile")

def main():
    """Main demo function"""
    try:
        run_benchmarking_demo()
        print(f"\n{'='*60}")
        print("✅ Demo completed successfully!")
        print("🚀 To run the full dashboard: python run_demo.py")
        print("📱 Or manually: streamlit run dashboard.py")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("💡 Make sure to install dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
