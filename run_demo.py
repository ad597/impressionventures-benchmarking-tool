#!/usr/bin/env python3
"""
Impression Ventures Competitive Benchmarking Tool - Demo Launcher
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import openai
        import langchain
        import faiss
        import pandas
        import plotly
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_environment():
    """Set up environment variables if not present"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("""# Impression Ventures Demo - Environment Variables
# Add your API keys here (optional for demo)

OPENAI_API_KEY=your_openai_api_key_here
CRUNCHBASE_API_KEY=your_crunchbase_api_key_here
LINKEDIN_API_KEY=your_linkedin_api_key_here
DATABASE_URL=sqlite:///benchmarking.db
""")
        print("✅ Created .env file - you can add your API keys if you have them")
    else:
        print("✅ .env file already exists")

def generate_sample_data():
    """Generate sample data for demo"""
    try:
        from sample_data_generator import generate_sample_companies, save_sample_data
        print("📊 Generating sample data...")
        companies = generate_sample_companies(50)
        save_sample_data(companies, "sample_companies.json")
        print(f"✅ Generated {len(companies)} sample companies")
        return True
    except Exception as e:
        print(f"⚠️  Could not generate sample data: {e}")
        return False

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Launching Impression Ventures Benchmarking Tool...")
    print("📱 The dashboard will open in your browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("\n" + "="*60)
    print("🎯 DEMO SCENARIOS TO TRY:")
    print("1. Company Analysis - Input metrics and see benchmarking")
    print("2. Industry Benchmarking - Analyze industry trends")
    print("3. Portfolio Overview - View portfolio performance")
    print("4. Data Extraction Demo - Upload documents for LLM extraction")
    print("="*60 + "\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        print("Try running manually: streamlit run dashboard.py")

def main():
    """Main demo launcher"""
    print("🚀 Impression Ventures Competitive Benchmarking Tool")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup environment
    setup_environment()
    
    # Generate sample data
    generate_sample_data()
    
    # Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main()
