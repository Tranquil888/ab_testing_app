# A/B Testing Desktop Application

A comprehensive desktop application for analyzing A/B test results using statistical methods and interactive visualizations.

## Features

- **Data Management**: Load, validate, and clean A/B test datasets
- **Probability Analysis**: Calculate conversion rates and basic statistics
- **Statistical Testing**: Monte Carlo simulation and z-test for hypothesis testing
- **Interactive Visualizations**: Histograms, comparison charts, and time series plots
- **Comprehensive Reporting**: Generate detailed analysis reports with recommendations
- **Export Capabilities**: Save results to CSV and plots to PNG/PDF

## Installation

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

```bash
python main.py
```

### Workflow

1. **Load Data**: 
   - Click "File" → "Load Data" or use Ctrl+O
   - Select your CSV file containing A/B test data
   - Required columns: `user_id`, `group`, `landing_page`, `converted`

2. **Clean Data**:
   - Click "Clean Data" to remove misaligned rows and duplicates
   - Review data information in the Data tab

3. **Run Analysis**:
   - **Probability Tab**: Calculate basic conversion statistics
   - **A/B Test Tab**: Run statistical tests (simulation and z-test)
   - **Visualizations Tab**: View interactive charts and plots
   - **Results Tab**: Generate comprehensive reports

4. **Export Results**:
   - Generate reports in the Results tab
   - Export data to CSV
   - Save plots as PNG or PDF

## Data Format

Your CSV file should contain the following columns:

- `user_id`: Unique identifier for each user
- `group`: Either 'control' or 'treatment'
- `landing_page`: Either 'old_page' or 'new_page'
- `converted`: 0 for no conversion, 1 for conversion
- `timestamp`: Date and time of the interaction (optional, for time analysis)

Optional country data file:
- `user_id`: User identifier
- `country`: Country code (e.g., 'US', 'UK', 'CA')

## Statistical Methods

### Monte Carlo Simulation
- Simulates 10,000 iterations under the null hypothesis
- Calculates p-value based on distribution of differences
- One-sided test: H₀: p_old - p_new ≥ 0, H₁: p_old - p_new < 0

### Z-Test for Proportions
- Uses statsmodels for statistical testing
- One-sided test comparing conversion rates
- Provides z-score and p-value

### Interpretation Guidelines
- p-value < 0.05: Statistically significant result
- p-value ≥ 0.05: Fail to reject null hypothesis
- Consider practical significance alongside statistical significance

## Application Structure

```
ab_testing_app/
├── main.py                 # Application entry point
├── requirements.txt         # Python dependencies
├── gui/
│   ├── __init__.py
│   └── main_window.py      # Main GUI interface
├── analysis/
│   ├── __init__.py
│   ├── data_processor.py   # Data loading and cleaning
│   └── ab_test_analyzer.py # Statistical analysis
├── visualization/
│   ├── __init__.py
│   └── plot_manager.py     # Matplotlib integration
└── utils/
    └── __init__.py
```

## Example Workflow

1. Load your A/B test data file
2. Clean the data to remove inconsistencies
3. Review probability statistics
4. Run A/B test simulation (10,000 iterations)
5. Run z-test for additional validation
6. View visualizations to understand results
7. Generate comprehensive report
8. Export results for documentation

## Troubleshooting

### Common Issues

1. **"Missing required columns"**: Ensure your CSV contains `user_id`, `group`, `landing_page`, `converted`
2. **"No data loaded"**: Load and clean data before running analysis
3. **Performance issues**: Large datasets may take time for simulation

### Tips

- Use the data preview to verify your data format
- Check the status bar for progress updates
- Save plots before closing the application
- Generate reports after completing all analyses

## Dependencies

- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `matplotlib`: Data visualization
- `statsmodels`: Statistical modeling and testing
- `scipy`: Scientific computing
- `tkinter`: GUI framework (built-in with Python)

## License

This application is provided for educational and research purposes.

## Support

For issues or questions, please refer to the documentation or check the error messages in the application status bar.
