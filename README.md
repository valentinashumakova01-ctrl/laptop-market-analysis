# Laptop Market Analysis

EDA and statistical analysis of the laptop market dataset.

## Project Goal

The goal of this project is to analyze laptop characteristics and identify which factors influence customer ratings.

The analysis includes:
- data cleaning
- feature engineering
- statistical analysis
- outlier detection
- visualization
- correlation analysis

## Dataset

Dataset: Laptop Selection Dataset

Features:
- laptop brand
- processor
- RAM
- storage
- operating system
- display size
- ratings
- reviews
- price

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Plotly

## Key Insights

### Hardware impact on ratings
- 16 GB RAM laptops receive significantly higher ratings
- SSD storage strongly outperforms HDD
- AMD processors show better average ratings than Intel

### Operating Systems
- macOS devices have the highest ratings
- Windows 11 dominates the market

### Optimal Mass-Market Configuration
- Windows 11
- Ryzen 5 / Intel i5
- 16 GB RAM
- 512 GB SSD

## Visualizations

### Correlation Matrix

![Correlation Matrix](images/correlation_matrix.png)

### Price vs Rating

![Price vs Rating](images/price_rating.png)

## Repository Structure

```bash
notebooks/      - Jupyter notebooks
src/            - preprocessing scripts
images/         - exported charts
```

## Future Improvements

- Build ML model for rating prediction
- Add clustering analysis
- Create Streamlit dashboard
- Deploy interactive app
