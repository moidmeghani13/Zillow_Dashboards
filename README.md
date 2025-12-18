# Zillow Dashboards

Interactive dashboards for visualizing Zillow housing data by ZIP code.

## Features
- ZIP-level time series (ZHVI)
- Year-over-year growth metrics
- Interactive maps and charts (Plotly + Dash)

## Setup
```bash
conda create -n zillow-dash python=3.11
conda activate zillow-dash
conda install -c conda-forge pandas plotly dash geopandas pyarrow
