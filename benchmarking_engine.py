import numpy as np
from typing import List, Dict, Any, Tuple
from models import Company, BenchmarkResult, RedFlag
from vector_database import CompanyVectorDatabase
from config import Config

class RedFlagDetector:
    """Detect red flags and outliers in company metrics"""
    
    def __init__(self):
        self.thresholds = {
            'arr': Config.ARR_THRESHOLD,
            'cac': Config.CAC_THRESHOLD,
            'ltv': Config.LTV_THRESHOLD,
            'churn_rate': Config.CHURN_THRESHOLD
        }
    
    def detect_red_flags(self, company: Company, benchmarks: Dict[str, float]) -> List[RedFlag]:
        """Detect red flags for a company based on benchmarks"""
        red_flags = []
        
        # ARR red flags
        if company.arr is not None:
            if company.arr < benchmarks.get('arr_p25', 0) * 0.5:
                red_flags.append(RedFlag(
                    flag_type="Low ARR",
                    severity="high",
                    description=f"ARR of ${company.arr:,.0f} is significantly below industry 25th percentile",
                    metric="arr",
                    value=company.arr,
                    threshold=benchmarks.get('arr_p25', 0),
                    recommendation="Focus on revenue growth and customer acquisition"
                ))
            elif company.arr > benchmarks.get('arr_p75', 0) * 2:
                red_flags.append(RedFlag(
                    flag_type="Unusually High ARR",
                    severity="medium",
                    description=f"ARR of ${company.arr:,.0f} is unusually high for stage",
                    metric="arr",
                    value=company.arr,
                    threshold=benchmarks.get('arr_p75', 0),
                    recommendation="Verify revenue metrics and business model sustainability"
                ))
        
        # CAC red flags
        if company.cac is not None:
            if company.cac > benchmarks.get('cac_p75', 0) * 2:
                red_flags.append(RedFlag(
                    flag_type="High CAC",
                    severity="high",
                    description=f"CAC of ${company.cac:,.0f} is significantly above industry 75th percentile",
                    metric="cac",
                    value=company.cac,
                    threshold=benchmarks.get('cac_p75', 0),
                    recommendation="Optimize customer acquisition channels and reduce CAC"
                ))
        
        # LTV red flags
        if company.ltv is not None:
            if company.ltv < benchmarks.get('ltv_p25', 0) * 0.5:
                red_flags.append(RedFlag(
                    flag_type="Low LTV",
                    severity="high",
                    description=f"LTV of ${company.ltv:,.0f} is significantly below industry 25th percentile",
                    metric="ltv",
                    value=company.ltv,
                    threshold=benchmarks.get('ltv_p25', 0),
                    recommendation="Improve customer retention and increase customer value"
                ))
        
        # LTV/CAC ratio red flags
        if company.ltv_cac_ratio is not None:
            if company.ltv_cac_ratio < 3:
                red_flags.append(RedFlag(
                    flag_type="Poor LTV/CAC Ratio",
                    severity="critical",
                    description=f"LTV/CAC ratio of {company.ltv_cac_ratio:.1f} is below sustainable threshold of 3:1",
                    metric="ltv_cac_ratio",
                    value=company.ltv_cac_ratio,
                    threshold=3.0,
                    recommendation="Critical: Either reduce CAC or increase LTV to achieve sustainable unit economics"
                ))
            elif company.ltv_cac_ratio > 10:
                red_flags.append(RedFlag(
                    flag_type="Unusually High LTV/CAC",
                    severity="medium",
                    description=f"LTV/CAC ratio of {company.ltv_cac_ratio:.1f} is unusually high",
                    metric="ltv_cac_ratio",
                    value=company.ltv_cac_ratio,
                    threshold=10.0,
                    recommendation="Verify LTV and CAC calculations for accuracy"
                ))
        
        # Churn rate red flags
        if company.churn_rate is not None:
            if company.churn_rate > benchmarks.get('churn_rate_p75', 0) * 1.5:
                red_flags.append(RedFlag(
                    flag_type="High Churn Rate",
                    severity="high",
                    description=f"Monthly churn rate of {company.churn_rate:.1%} is significantly above industry 75th percentile",
                    metric="churn_rate",
                    value=company.churn_rate,
                    threshold=benchmarks.get('churn_rate_p75', 0),
                    recommendation="Implement customer retention strategies and improve product-market fit"
                ))
        
        # Growth rate red flags
        if company.growth_rate is not None:
            if company.growth_rate < 0.05:  # Less than 5% monthly growth
                red_flags.append(RedFlag(
                    flag_type="Low Growth Rate",
                    severity="medium",
                    description=f"Monthly growth rate of {company.growth_rate:.1%} is below healthy threshold",
                    metric="growth_rate",
                    value=company.growth_rate,
                    threshold=0.05,
                    recommendation="Focus on growth strategies and market expansion"
                ))
        
        return red_flags
    
    def calculate_risk_score(self, red_flags: List[RedFlag]) -> float:
        """Calculate overall risk score based on red flags"""
        if not red_flags:
            return 0.0
        
        severity_weights = {
            "low": 0.2,
            "medium": 0.4,
            "high": 0.7,
            "critical": 1.0
        }
        
        total_weight = sum(severity_weights.get(flag.severity, 0.5) for flag in red_flags)
        max_possible_weight = len(red_flags) * 1.0
        
        return min(total_weight / max_possible_weight, 1.0)

class BenchmarkingEngine:
    """Main benchmarking engine for comparing companies"""
    
    def __init__(self, vector_db: CompanyVectorDatabase):
        self.vector_db = vector_db
        self.red_flag_detector = RedFlagDetector()
    
    def benchmark_company(self, company: Company, num_peers: int = 10) -> BenchmarkResult:
        """Benchmark a company against similar peers"""
        # Find similar companies
        similar_companies = self.vector_db.search_similar(company, k=num_peers)
        peer_companies = [peer[0] for peer in similar_companies]
        
        # Get industry benchmarks
        industry_benchmarks = self.vector_db.get_industry_benchmarks(company.industry)
        
        # Calculate metrics comparison
        metrics_comparison = self._calculate_metrics_comparison(company, peer_companies, industry_benchmarks)
        
        # Detect red flags
        red_flags = self.red_flag_detector.detect_red_flags(company, industry_benchmarks)
        
        # Calculate risk score
        risk_score = self.red_flag_detector.calculate_risk_score(red_flags)
        
        # Generate insights
        insights = self._generate_insights(company, peer_companies, metrics_comparison, red_flags)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(risk_score, red_flags, metrics_comparison)
        
        return BenchmarkResult(
            company=company,
            peer_companies=peer_companies,
            metrics_comparison=metrics_comparison,
            red_flags=[flag.description for flag in red_flags],
            insights=insights,
            risk_score=risk_score,
            recommendation=recommendation
        )
    
    def _calculate_metrics_comparison(self, company: Company, peers: List[Company], benchmarks: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Calculate detailed metrics comparison"""
        comparison = {}
        
        metrics = ['arr', 'cac', 'ltv', 'ltv_cac_ratio', 'churn_rate', 'growth_rate']
        
        for metric in metrics:
            company_value = getattr(company, metric)
            if company_value is None:
                continue
            
            peer_values = [getattr(peer, metric) for peer in peers if getattr(peer, metric) is not None]
            
            if not peer_values:
                continue
            
            peer_median = np.median(peer_values)
            peer_mean = np.mean(peer_values)
            peer_p25 = np.percentile(peer_values, 25)
            peer_p75 = np.percentile(peer_values, 75)
            
            # Calculate percentiles
            company_percentile = self._calculate_percentile(company_value, peer_values)
            
            comparison[metric] = {
                'company_value': company_value,
                'peer_median': peer_median,
                'peer_mean': peer_mean,
                'peer_p25': peer_p25,
                'peer_p75': peer_p75,
                'company_percentile': company_percentile,
                'vs_median': (company_value - peer_median) / peer_median if peer_median != 0 else 0,
                'vs_mean': (company_value - peer_mean) / peer_mean if peer_mean != 0 else 0
            }
        
        return comparison
    
    def _calculate_percentile(self, value: float, values: List[float]) -> float:
        """Calculate percentile rank of value in values"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        count_below = sum(1 for v in sorted_values if v < value)
        return (count_below / len(sorted_values)) * 100
    
    def _generate_insights(self, company: Company, peers: List[Company], metrics_comparison: Dict[str, Dict[str, Any]], red_flags: List[RedFlag]) -> List[str]:
        """Generate insights from benchmarking analysis"""
        insights = []
        
        # ARR insights
        if 'arr' in metrics_comparison:
            arr_data = metrics_comparison['arr']
            if arr_data['company_percentile'] > 75:
                insights.append(f"Strong ARR performance: ${company.arr:,.0f} is in the top 25% of similar companies")
            elif arr_data['company_percentile'] < 25:
                insights.append(f"ARR growth opportunity: ${company.arr:,.0f} is below 75% of similar companies")
        
        # LTV/CAC insights
        if 'ltv_cac_ratio' in metrics_comparison:
            ltv_cac_data = metrics_comparison['ltv_cac_ratio']
            if ltv_cac_data['company_value'] > 5:
                insights.append(f"Excellent unit economics: LTV/CAC ratio of {company.ltv_cac_ratio:.1f} indicates strong profitability potential")
            elif ltv_cac_data['company_value'] < 3:
                insights.append(f"Unit economics concern: LTV/CAC ratio of {company.ltv_cac_ratio:.1f} may indicate unsustainable growth")
        
        # Growth insights
        if 'growth_rate' in metrics_comparison:
            growth_data = metrics_comparison['growth_rate']
            if growth_data['company_percentile'] > 75:
                insights.append(f"Exceptional growth: {company.growth_rate:.1%} monthly growth is in the top 25% of peers")
            elif growth_data['company_percentile'] < 25:
                insights.append(f"Growth acceleration needed: {company.growth_rate:.1%} monthly growth is below 75% of peers")
        
        # Churn insights
        if 'churn_rate' in metrics_comparison:
            churn_data = metrics_comparison['churn_rate']
            if churn_data['company_percentile'] < 25:
                insights.append(f"Excellent retention: {company.churn_rate:.1%} monthly churn is in the bottom 25% (best retention)")
            elif churn_data['company_percentile'] > 75:
                insights.append(f"Retention improvement needed: {company.churn_rate:.1%} monthly churn is in the top 25% (highest churn)")
        
        return insights
    
    def _generate_recommendation(self, risk_score: float, red_flags: List[RedFlag], metrics_comparison: Dict[str, Dict[str, Any]]) -> str:
        """Generate investment recommendation"""
        if risk_score > 0.7:
            return "HIGH RISK - Multiple red flags detected. Proceed with extreme caution or consider passing."
        elif risk_score > 0.4:
            return "MEDIUM RISK - Some concerns identified. Requires additional due diligence and monitoring."
        elif risk_score > 0.2:
            return "LOW RISK - Minor concerns. Standard due diligence recommended."
        else:
            return "LOW RISK - Strong metrics across the board. Consider for investment with standard monitoring."
    
    def get_industry_analysis(self, industry: str) -> Dict[str, Any]:
        """Get comprehensive industry analysis"""
        industry_companies = self.vector_db.search_by_criteria(industry=industry)
        
        if not industry_companies:
            return {"error": f"No companies found for industry: {industry}"}
        
        # Calculate industry statistics
        arrs = [c.arr for c in industry_companies if c.arr is not None]
        cacs = [c.cac for c in industry_companies if c.cac is not None]
        ltvs = [c.ltv for c in industry_companies if c.ltv is not None]
        churn_rates = [c.churn_rate for c in industry_companies if c.churn_rate is not None]
        growth_rates = [c.growth_rate for c in industry_companies if c.growth_rate is not None]
        
        analysis = {
            "total_companies": len(industry_companies),
            "arr_stats": self._calculate_stats(arrs),
            "cac_stats": self._calculate_stats(cacs),
            "ltv_stats": self._calculate_stats(ltvs),
            "churn_stats": self._calculate_stats(churn_rates),
            "growth_stats": self._calculate_stats(growth_rates)
        }
        
        return analysis
    
    def _calculate_stats(self, values: List[float]) -> Dict[str, float]:
        """Calculate statistical measures for a list of values"""
        if not values:
            return {}
        
        return {
            "count": len(values),
            "mean": np.mean(values),
            "median": np.median(values),
            "std": np.std(values),
            "min": np.min(values),
            "max": np.max(values),
            "p25": np.percentile(values, 25),
            "p75": np.percentile(values, 75)
        }
