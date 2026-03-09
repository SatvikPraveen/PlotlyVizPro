# 🔧 Troubleshooting Guide

Common issues and their solutions for PlotlyVizPro.

---

## Table of Contents

- [Installation Issues](#installation-issues)
- [Jupyter Notebook Issues](#jupyter-notebook-issues)
- [Plotly Rendering Issues](#plotly-rendering-issues)
- [Streamlit Issues](#streamlit-issues)
- [Data Loading Issues](#data-loading-issues)
- [Export Issues](#export-issues)
- [Docker Issues](#docker-issues)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### Problem: `pip install` fails with dependency conflicts

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Use fresh virtual environment
python3 -m venv venv_fresh
source venv_fresh/bin/activate
pip install -r requirements.txt

# If still failing, install one by one
pip install pandas numpy
pip install plotly
pip install streamlit
# ... etc
```

### Problem: `ModuleNotFoundError: No module named 'plotly'`

**Cause:** Wrong Python environment or installation failed

**Solution:**
```bash
# Verify you're in virtual environment
which python  # Should show venv/bin/python

# Check installed packages
pip list | grep plotly

# Reinstall if missing
pip install plotly
```

### Problem: Kaleido installation fails on Apple Silicon (M1/M2)

**Solution:**
```bash
# Use conda for M1/M2 Macs
conda install -c conda-forge python-kaleido

# Or use arm64 compatible version
pip install kaleido --no-binary kaleido
```

---

## Jupyter Notebook Issues

### Problem: Jupyter doesn't start or shows blank page

**Solution:**
```bash
# Clear Jupyter cache
jupyter --data-dir  # Shows cache location
rm -rf ~/.jupyter

# Reinstall Jupyter
pip uninstall jupyter jupyterlab
pip install jupyterlab

# Start with specific browser
jupyter lab --browser=chrome
```

### Problem: Plotly plots don't render in Jupyter

**Cause:** JupyterLab extensions not enabled or renderer issue

**Solution:**
```bash
# Check JupyterLab version
jupyter lab --version  # Should be 3.0+

# For older versions, install extension
jupyter labextension install jupyterlab-plotly

# In notebook, try different renderer
import plotly.io as pio
pio.renderers.default = 'iframe'  # or 'notebook' or 'colab'
```

### Problem: Notebook cells won't execute

**Solution:**
```bash
# Restart kernel
# In Jupyter: Kernel > Restart Kernel

# Check if kernel is running
jupyter kernelspec list

# Reinstall kernel
python -m ipykernel install --user
```

### Problem: `OSError: [Errno 48] Address already in use`

**Cause:** Port 8888 already in use

**Solution:**
```bash
# Find process using port
lsof -i :8888

# Kill the process
kill -9 <PID>

# Or use different port
jupyter lab --port 8889
```

---

## Plotly Rendering Issues

### Problem: Plot shows but is blank/empty

**Cause:** Data issues or incorrect column names

**Solution:**
```python
# Debug data
print(df.head())
print(df.columns)
print(df.dtypes)

# Check for NaN values
print(df.isnull().sum())

# Verify column names match exactly (case-sensitive!)
fig = px.line(df, x='Date', y='Sales')  # Ensure 'Date' and 'Sales' exist
```

### Problem: `ValueError: Invalid property specified`

**Cause:** Incorrect parameter passed to Plotly

**Solution:**
```python
# Common mistakes:
# 1. Wrong parameter name
fig = px.scatter(df, x='Sales', y='Profit', color='Category')  # ✓
# Not: fig = px.scatter(df, x='Sales', y='Profit', colour='Category')  # ✗

# 2. Check Plotly documentation
import plotly.express as px
help(px.scatter)
```

### Problem: Dates not displaying correctly

**Solution:**
```python
# Convert to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Specify format if needed
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# For plots
fig = px.line(df, x='Date', y='Sales')
fig.update_xaxes(tickformat='%b %Y')  # Format as 'Jan 2024'
```

### Problem: Colors not showing or all the same

**Solution:**
```python
# Ensure color column has distinct values
print(df['Category'].unique())

# Explicitly set color scale
fig = px.scatter(
    df, x='Sales', y='Profit',
    color='Category',
    color_discrete_sequence=px.colors.qualitative.Plotly
)

# For continuous colors
fig = px.scatter(
    df, x='Sales', y='Profit',
    color='Profit',
    color_continuous_scale='Viridis'
)
```

---

## Streamlit Issues

### Problem: `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
pip install streamlit

# Verify installation
streamlit --version
```

### Problem: App doesn't update when code changes

**Cause:** Streamlit caching or not watching files

**Solution:**
```python
# Clear cache in app
st.cache_data.clear()

# Or rerun from command line
# Press 'R' in terminal or 'Always rerun' in browser
```

### Problem: `Port 8501 is already in use`

**Solution:**
```bash
# Find process
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

### Problem: Plots don't show in Streamlit

**Solution:**
```python
# Use st.plotly_chart() not fig.show()
import streamlit as st

fig = px.line(df, x='Date', y='Sales')
st.plotly_chart(fig, use_container_width=True)  # ✓
# Not: fig.show()  # ✗ (won't work in Streamlit)
```

### Problem: Layout issues or overlapping elements

**Solution:**
```python
# Use columns
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1)
with col2:
    st.plotly_chart(fig2)

# Use containers
with st.container():
    st.write("Section 1")
    st.plotly_chart(fig)

# Use expanders for collapsible sections
with st.expander("Show Details"):
    st.write(df)
```

---

## Data Loading Issues

### Problem: `FileNotFoundError: datasets/superstore.csv`

**Cause:** Running from wrong directory

**Solution:**
```bash
# Always run from project root
cd PlotlyVizPro
python generate_datasets.py
streamlit run app.py

# Or use absolute paths in code
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
df = pd.read_csv(PROJECT_ROOT / 'datasets' / 'superstore.csv')
```

### Problem: CSV parsing errors

**Solution:**
```python
# Specify encoding
df = pd.read_csv('datasets/superstore.csv', encoding='utf-8')

# Handle different separators
df = pd.read_csv('file.csv', sep=';')  # If semicolon-separated

# Skip bad lines
df = pd.read_csv('file.csv', error_bad_lines=False, warn_bad_lines=True)
```

### Problem: Datasets not generated

**Solution:**
```bash
# Generate datasets manually
python generate_datasets.py

# Or use Makefile
make generate-data

# Check if faker is installed
pip install faker
```

---

## Export Issues

### Problem: `save_fig_as_png()` fails with Kaleido error

**Cause:** Kaleido not installed or incompatible

**Solution:**
```bash
# Reinstall kaleido
pip uninstall kaleido
pip install kaleido

# For M1/M2 Macs
conda install -c conda-forge python-kaleido

# Verify kaleido works
python -c "import kaleido; print(kaleido.__version__)"
```

### Problem: Exported HTML doesn't show plots

**Cause:** Missing plotly.js or incorrect path

**Solution:**
```python
# Include plotly.js in HTML
fig.write_html(
    'plot.html',
    include_plotlyjs='cdn'  # or 'directory' or True
)

# Full standalone HTML
fig.write_html('plot.html', include_plotlyjs=True)
```

### Problem: PNG export shows low quality

**Solution:**
```python
# Increase resolution
fig.write_image(
    'plot.png',
    width=1920,
    height=1080,
    scale=2  # 2x resolution
)
```

---

## Docker Issues

### Problem: Docker build fails

**Solution:**
```bash
# Check Docker is running
docker --version

# Build with no cache
docker build --no-cache -t plotlyvizpro .

# Check build logs
docker build -t plotlyvizpro . 2>&1 | tee build.log
```

### Problem: Container exits immediately

**Solution:**
```bash
# Check logs
docker logs <container_id>

# Run interactively
docker run -it plotlyvizpro /bin/bash

# Check ENTRYPOINT/CMD
docker inspect plotlyvizpro
```

### Problem: Can't access Jupyter in Docker

**Solution:**
```bash
# Ensure port mapping
docker run -p 8888:8888 plotlyvizpro

# Check if service is running inside container
docker exec -it <container_id> netstat -tulpn | grep 8888

# Get Jupyter token
docker logs <container_id> | grep token
```

---

## Performance Issues

### Problem: Plots take too long to render

**Solution:**
```python
# Reduce data points
df_sampled = df.sample(frac=0.1)  # Use 10% of data

# Use simpler plot types
# Instead of: fig = px.scatter(large_df, ...)
# Use: fig = px.scatter(df.sample(10000), ...)

# Disable hover for large datasets
fig.update_traces(hoverinfo='skip')
```

### Problem: Streamlit app is slow

**Solution:**
```python
# Use caching aggressively
@st.cache_data
def load_data():
    return pd.read_csv('large_file.csv')

@st.cache_resource
def create_expensive_plot(df):
    return px.scatter_3d(df, ...)

# Lazy load data
if st.button('Load Analysis'):
    df = load_heavy_data()
```

### Problem: Memory errors with large datasets

**Solution:**
```python
# Read in chunks
chunks = pd.read_csv('large.csv', chunksize=10000)
df = pd.concat([chunk for chunk in chunks if chunk['Date'] > '2024-01-01'])

# Use more memory-efficient dtypes
df['Category'] = df['Category'].astype('category')
df['Date'] = pd.to_datetime(df['Date'])

# Delete unused variables
del large_df
import gc
gc.collect()
```

---

## Testing Issues

### Problem: Tests fail with import errors

**Solution:**
```bash
# Install dev dependencies
pip install -r requirements_dev.txt
pip install pytest pytest-cov

# Run from project root
cd PlotlyVizPro
pytest tests/

# If path issues, add to PYTHONPATH
export PYTHONPATH=$PWD:$PYTHONPATH
pytest tests/
```

### Problem: Coverage report not generated

**Solution:**
```bash
# Install pytest-cov
pip install pytest-cov

# Run with coverage
pytest tests/ --cov=utils --cov-report=html

# View report
open htmlcov/index.html
```

---

## Getting More Help

If your issue isn't listed here:

1. **Check the documentation**: Read [API.md](API.md) and [TUTORIALS.md](TUTORIALS.md)
2. **Search issues**: Look at [GitHub Issues](https://github.com/SatvikPraveen/PlotlyVizPro/issues)
3. **Ask for help**: Open a new issue with:
   - Your OS and Python version
   - Full error message
   - Minimal code to reproduce
   - What you've already tried

4. **Useful commands for debugging**:
```bash
# System info
python --version
pip --version
jupyter --version
streamlit --version

# Package versions
pip list

# Check installation
python -c "import plotly; print(plotly.__version__)"
python -c "import streamlit; print(streamlit.__version__)"
```

---

**Last Updated:** March 9, 2026
