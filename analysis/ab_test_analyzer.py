import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import norm
from typing import Tuple, Dict, Any

class ABTestAnalyzer:
    """Performs A/B testing analysis including simulation and statistical tests."""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.simulation_results = None
        self.z_test_results = None
    
    def run_simulation(self, n_iterations: int = 10000) -> Dict[str, Any]:
        """Run Monte Carlo simulation under null hypothesis."""
        if self.data_processor.df_clean is None:
            return {'error': 'No data available'}
        
        # Get data parameters
        stats = self.data_processor.get_probability_stats()
        sizes = self.data_processor.get_sample_sizes()
        
        p_null = stats['overall_conversion']
        n_new = sizes.get('n_new', 0)
        n_old = sizes.get('n_old', 0)
        
        if n_new == 0 or n_old == 0:
            return {'error': 'Invalid sample sizes'}
        
        # Run simulation
        np.random.seed(42)  # For reproducibility
        p_diffs = (np.random.binomial(n_new, p_null, n_iterations) / n_new - 
                  np.random.binomial(n_old, p_null, n_iterations) / n_old)
        
        # Calculate actual difference
        actual_diff = stats['treatment_conversion'] - stats['control_conversion']
        
        # Calculate p-value
        p_value = (p_diffs > actual_diff).mean()
        
        self.simulation_results = {
            'p_diffs': p_diffs,
            'actual_diff': actual_diff,
            'p_value': p_value,
            'p_null': p_null,
            'n_iterations': n_iterations
        }
        
        return self.simulation_results
    
    def run_z_test(self) -> Dict[str, Any]:
        """Run z-test for proportions."""
        if self.data_processor.df_clean is None:
            return {'error': 'No data available'}
        
        counts = self.data_processor.get_conversion_counts()
        sizes = self.data_processor.get_sample_sizes()
        
        convert_new = counts.get('convert_new', 0)
        convert_old = counts.get('convert_old', 0)
        n_new = sizes.get('n_new', 0)
        n_old = sizes.get('n_old', 0)
        
        if n_new == 0 or n_old == 0:
            return {'error': 'Invalid sample sizes'}
        
        # Run z-test (one-sided: new > old)
        z_score, p_value = sm.stats.proportions_ztest(
            [convert_new, convert_old], 
            [n_new, n_old], 
            alternative='larger'
        )
        
        # Critical value for one-sided test at 95% confidence
        critical_value = norm.ppf(1 - 0.05)
        z_significance = norm.cdf(z_score)
        
        self.z_test_results = {
            'z_score': z_score,
            'p_value': p_value,
            'critical_value': critical_value,
            'z_significance': z_significance,
            'convert_new': convert_new,
            'convert_old': convert_old,
            'n_new': n_new,
            'n_old': n_old
        }
        
        return self.z_test_results
    
    def get_interpretation(self) -> str:
        """Get interpretation of test results."""
        if self.simulation_results is None and self.z_test_results is None:
            return "No test results available. Please run analysis first."
        
        interpretation = []
        
        if self.simulation_results:
            p_val_sim = self.simulation_results['p_value']
            interpretation.append(f"Simulation p-value: {p_val_sim:.4f}")
            
            if p_val_sim > 0.05:
                interpretation.append("→ Fail to reject null hypothesis")
                interpretation.append("→ New page is NOT significantly better than old page")
            else:
                interpretation.append("→ Reject null hypothesis")
                interpretation.append("→ New page shows significant improvement")
        
        if self.z_test_results:
            p_val_z = self.z_test_results['p_value']
            z_score = self.z_test_results['z_score']
            critical_value = self.z_test_results['critical_value']
            
            interpretation.append(f"\nZ-test p-value: {p_val_z:.4f}")
            interpretation.append(f"Z-score: {z_score:.4f} (critical: {critical_value:.4f})")
            
            if z_score < critical_value and p_val_z > 0.05:
                interpretation.append("→ Fail to reject null hypothesis")
                interpretation.append("→ No statistically significant difference")
            else:
                interpretation.append("→ Statistically significant result detected")
        
        return "\n".join(interpretation)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for reporting."""
        if self.data_processor.df_clean is None:
            return {}
        
        stats = self.data_processor.get_probability_stats()
        sizes = self.data_processor.get_sample_sizes()
        
        summary = {
            'total_users': len(self.data_processor.df_clean),
            'unique_users': self.data_processor.df_clean['user_id'].nunique(),
            'overall_conversion_rate': stats['overall_conversion'],
            'control_conversion_rate': stats['control_conversion'],
            'treatment_conversion_rate': stats['treatment_conversion'],
            'conversion_difference': stats['treatment_conversion'] - stats['control_conversion'],
            'new_page_sample_size': sizes.get('n_new', 0),
            'old_page_sample_size': sizes.get('n_old', 0)
        }
        
        return summary
