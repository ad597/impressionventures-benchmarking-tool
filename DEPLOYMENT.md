# 🚀 Deployment Guide

## Deploy to GitHub

### Option 1: Using GitHub CLI (Recommended)
```bash
# Install GitHub CLI if not already installed
# macOS: brew install gh
# Or download from: https://cli.github.com/

# Login to GitHub
gh auth login

# Create repository and push
gh repo create impressionventures-benchmarking-tool --public --description "AI-powered competitive benchmarking tool for venture capital due diligence"
git remote add origin https://github.com/ad597/impressionventures-benchmarking-tool.git
git branch -M main
git push -u origin main
```

### Option 2: Manual GitHub Setup
1. Go to [GitHub.com](https://github.com) and create a new repository
2. Name it: `impressionventures-benchmarking-tool`
3. Make it public
4. Don't initialize with README (we already have one)
5. Run these commands:

```bash
git remote add origin https://github.com/ad597/impressionventures-benchmarking-tool.git
git branch -M main
git push -u origin main
```

### Option 3: Deploy to GitHub Pages (For Demo)
```bash
# Create a simple HTML demo page
echo '<!DOCTYPE html>
<html>
<head>
    <title>Impression Ventures Benchmarking Tool</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .demo-button { 
            background: #1f77b4; color: white; padding: 15px 30px; 
            text-decoration: none; border-radius: 5px; display: inline-block;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Impression Ventures Competitive Benchmarking Tool</h1>
        <p>AI-powered competitive benchmarking tool for venture capital due diligence.</p>
        
        <h2>🎯 Features</h2>
        <ul>
            <li>LLM-powered data extraction from pitch decks, websites, and SEC filings</li>
            <li>FAISS vector database for company similarity search</li>
            <li>Real-time benchmarking engine with red flag detection</li>
            <li>Interactive Streamlit dashboard</li>
            <li>API integrations for Crunchbase, LinkedIn, and fintech data</li>
        </ul>
        
        <h2>🚀 Quick Start</h2>
        <pre><code># Clone the repository
git clone https://github.com/ad597/impressionventures-benchmarking-tool.git
cd impressionventures-benchmarking-tool

# Install dependencies
pip install -r requirements.txt

# Run the demo
python run_demo.py</code></pre>
        
        <a href="https://github.com/ad597/impressionventures-benchmarking-tool" class="demo-button">
            View on GitHub
        </a>
    </div>
</body>
</html>' > index.html

# Add and commit
git add index.html
git commit -m "Add GitHub Pages demo page"
git push origin main
```

## 🌐 Live Demo Options

### Option 1: Streamlit Cloud (Free)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Deploy automatically
4. Get a live URL like: `https://your-app.streamlit.app`

### Option 2: Heroku (Free Tier)
```bash
# Create Procfile
echo "web: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Create runtime.txt
echo "python-3.9.18" > runtime.txt

# Add and commit
git add Procfile runtime.txt
git commit -m "Add Heroku deployment files"
git push origin main

# Deploy to Heroku
heroku create impressionventures-benchmarking
git push heroku main
```

### Option 3: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

## 📱 Demo Instructions

Once deployed, you can share:

1. **GitHub Repository**: `https://github.com/ad597/impressionventures-benchmarking-tool`
2. **Live Demo**: `https://your-app.streamlit.app` (if using Streamlit Cloud)
3. **Local Demo**: Clone and run `python run_demo.py`

## 🎯 Interview Demo Flow

1. **Show the Problem**: "Post-screening due diligence is slowed by manual benchmarking"
2. **Present the Solution**: "Built an AI-powered competitive benchmarking tool"
3. **Live Demo**: 
   - Upload a pitch deck → Extract metrics
   - Input company data → Get benchmarking results
   - Show red flag detection → Investment recommendation
4. **Technical Deep Dive**: Explain LLM pipelines, vector databases, API integrations
5. **Business Impact**: "Cuts benchmarking time from hours to minutes"

## 🔧 Environment Setup for Demo

```bash
# Quick setup for interview demo
git clone https://github.com/ad597/impressionventures-benchmarking-tool.git
cd impressionventures-benchmarking-tool
pip install -r requirements.txt
python run_demo.py
```

The tool will:
- Generate sample data automatically
- Launch the Streamlit dashboard
- Show all demo scenarios
- Be ready for live demonstration
