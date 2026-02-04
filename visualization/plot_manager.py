import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from typing import Optional, Dict, Any

class PlotManager:
    """Manages matplotlib plots for the A/B testing application."""
    
    def __init__(self):
        self.figures = {}
        self.canvases = {}
    
    def create_simulation_histogram(self, parent_frame, simulation_data: Dict[str, Any]) -> FigureCanvasTkAgg:
        """Create histogram of simulation results."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        p_diffs = simulation_data['p_diffs']
        actual_diff = simulation_data['actual_diff']
        
        # Create histogram
        ax.hist(p_diffs, bins=200, alpha=0.7, color='skyblue', edgecolor='black')
        
        # Add vertical line for actual difference
        ax.axvline(actual_diff, color='red', linewidth=2, label=f'Actual Difference: {actual_diff:.6f}')
        ax.axvline(0, color='black', linestyle='--', alpha=0.5, label='Null Hypothesis (0)')
        
        # Formatting
        ax.set_xlabel('Difference in Conversion Rates (p_new - p_old)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Distribution of Simulated Differences Under Null Hypothesis', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Set reasonable x-limits
        ax.set_xlim(-0.005, 0.005)
        
        # Add p-value annotation
        p_value = simulation_data['p_value']
        ax.text(0.02, 0.98, f'P-value: {p_value:.4f}', 
                transform=ax.transAxes, fontsize=12,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        
        self.figures['simulation'] = fig
        self.canvases['simulation'] = canvas
        
        return canvas
    
    def create_conversion_comparison_chart(self, parent_frame, stats: Dict[str, Any]) -> FigureCanvasTkAgg:
        """Create bar chart comparing conversion rates."""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        groups = ['Control\n(Old Page)', 'Treatment\n(New Page)']
        conversion_rates = [stats['control_conversion'], stats['treatment_conversion']]
        colors = ['lightcoral', 'lightblue']
        
        bars = ax.bar(groups, conversion_rates, color=colors, alpha=0.8, edgecolor='black')
        
        # Add value labels on bars
        for bar, rate in zip(bars, conversion_rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                   f'{rate:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Formatting
        ax.set_ylabel('Conversion Rate', fontsize=12)
        ax.set_title('Conversion Rate Comparison: Control vs Treatment', fontsize=14, fontweight='bold')
        ax.set_ylim(0, max(conversion_rates) * 1.2)
        
        # Add grid
        ax.grid(True, alpha=0.3, axis='y')
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        
        self.figures['comparison'] = fig
        self.canvases['comparison'] = canvas
        
        return canvas
    
    def create_time_series_plot(self, parent_frame, time_data: pd.DataFrame) -> FigureCanvasTkAgg:
        """Create time series plot of conversion rates over time."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot 1: Conversion rates over time
        ax1.scatter(time_data['day'], time_data['old_rate'], 
                   color='green', label='Old Page', alpha=0.7, s=50)
        ax1.scatter(time_data['day'], time_data['new_rate'], 
                   color='red', label='New Page', alpha=0.7, s=50)
        
        ax1.set_xlabel('Day of Month', fontsize=11)
        ax1.set_ylabel('Conversion Rate', fontsize=11)
        ax1.set_title('Conversion Rates Over Time', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Difference over time
        ax2.scatter(time_data['day'], time_data['new_rate'] - time_data['old_rate'], 
                   color='blue', alpha=0.7, s=50)
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        ax2.set_xlabel('Day of Month', fontsize=11)
        ax2.set_ylabel('Difference (New - Old)', fontsize=11)
        ax2.set_title('Conversion Rate Difference Over Time', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        
        self.figures['time_series'] = fig
        self.canvases['time_series'] = canvas
        
        return canvas
    
    def create_day_of_week_chart(self, parent_frame, dow_data: pd.DataFrame) -> FigureCanvasTkAgg:
        """Create bar chart for day of week conversion rates."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        days = dow_data.index.tolist()
        rates = dow_data['conversion_rate'].values
        
        # Create color gradient
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(days)))
        
        bars = ax.bar(days, rates, color=colors, alpha=0.8, edgecolor='black')
        
        # Add value labels
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.0005,
                   f'{rate:.4f}', ha='center', va='bottom', fontsize=10, rotation=45)
        
        # Formatting
        ax.set_ylabel('Conversion Rate', fontsize=12)
        ax.set_title('Conversion Rates by Day of Week', fontsize=14, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        
        self.figures['day_of_week'] = fig
        self.canvases['day_of_week'] = canvas
        
        return canvas
    
    def clear_all_plots(self):
        """Clear all stored figures and canvases."""
        for fig in self.figures.values():
            plt.close(fig)
        
        self.figures.clear()
        self.canvases.clear()
    
    def save_plot(self, plot_name: str, filename: str):
        """Save a specific plot to file."""
        if plot_name in self.figures:
            self.figures[plot_name].savefig(filename, dpi=300, bbox_inches='tight')
            return True
        return False
