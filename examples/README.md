# 📚 PlotlyVizPro Examples

Standalone Python scripts demonstrating specific Plotly use cases. These complement the Jupyter notebooks with quick, runnable examples.

---

## 📂 Directory Structure

```
examples/
├── 01_quick_starts/          # Minimal starter scripts (< 20 lines)
├── 02_recipes/               # Task-specific solutions
├── 03_integrations/          # Combining multiple concepts
├── 04_advanced/              # Advanced patterns and techniques
└── README.md                 # This file
```

---

## 🚀 Quick Start Examples

**Purpose**: Get a plot running in under 20 lines of code.

| Script | Description | Lines |
|--------|-------------|-------|
| `basic_line.py` | Simple line plot | ~10 |
| `basic_scatter.py` | Simple scatter plot | ~10 |
| `basic_bar.py` | Basic bar chart | ~10 |
| `dark_theme_plot.py` | Apply dark theme | ~12 |
| `save_plot.py` | Export HTML/PNG | ~15 |

**Usage:**
```bash
cd examples/01_quick_starts
python basic_line.py
```

---

## 🧑‍🍳 Recipe Examples

**Purpose**: Solve specific visualization tasks.

| Script | Description | Use Case |
|--------|-------------|----------|
| `compare_categories.py` | Compare metrics across categories | Business analysis |
| `time_series_trend.py` | Time series with moving average | Financial tracking |
| `correlation_heatmap.py` | Correlation matrix visualization | Data exploration |
| `multi_metric_dashboard.py` | Multiple metrics in one view | Reporting |
| `interactive_filter.py` | Interactive dropdowns/sliders | Dashboards |

**Usage:**
```bash
cd examples/02_recipes
python compare_categories.py
# Opens interactive plot in browser
```

---

## 🔗 Integration Examples

**Purpose**: Combine multiple Plotly features.

| Script | Description | Combines |
|--------|-------------|----------|
| `dashboard_layout.py` | 2x2 subplot grid | Subplots + Multiple chart types |
| `animated_time_series.py` | Animated sales by region | Animation + Time series |
| `geographic_stats.py` | Map with statistics overlay | Choropleth + Annotations |
| `custom_theme_pipeline.py` | Themed multi-panel dashboard | Theming + Layouts + Export |

---

## 🎓 Advanced Examples

**Purpose**: Advanced patterns and best practices.

| Script | Description | Demonstrates |
|--------|-------------|--------------|
| `parametric_plotting.py` | Function-based plot generation | Abstraction patterns |
| `data_pipeline_viz.py` | Full ETL → Viz pipeline | Data engineering |
| `realtime_simulation.py` | Simulated live data updates | Dynamic updates |
| `custom_interactions.py` | Custom hover, click behaviors | Advanced interactivity |
| `performance_optimization.py` | Large dataset handling | Performance tuning |

---

## 🎯 How Examples Differ from Notebooks

| Aspect | Notebooks | Examples |
|--------|-----------|----------|
| **Purpose** | Learn concepts step-by-step | Quick reference & solutions |
| **Format** | Markdown + Code + Outputs | Pure Python scripts |
| **Length** | Comprehensive (100+ lines) | Focused (10-50 lines) |
| **Execution** | Interactive cells | Run entire script |
| **Documentation** | Inline explanations | Comments only |
| **Target** | Learners studying Plotly | Practitioners needing quick solutions |

---

## 💡 When to Use What

### Use Notebooks When:
- 📖 Learning Plotly concepts from scratch
- 🧪 Experimenting with different parameters
- 📝 Documenting your analysis process
- 🎓 Teaching or presenting concepts

### Use Examples When:
- ⚡ Need a quick solution to copy
- 🔧 Building similar functionality in your project
- 📋 Creating a new script from a template
- 🚀 Getting started fast without reading full tutorials

---

## 🛠️ Running Examples

### Individual Script
```bash
# Navigate to examples directory
cd examples/01_quick_starts

# Run any script
python basic_line.py

# Most scripts will:
# 1. Load/generate data
# 2. Create visualization
# 3. Open in browser (fig.show())
# 4. Optionally save to exports/
```

### With Custom Data
```bash
# Many scripts accept command-line arguments
python compare_categories.py --data /path/to/your/data.csv --column Sales
```

### Batch Run
```bash
# Run all quick starts
cd examples/01_quick_starts
for script in *.py; do python "$script"; done
```

---

## 📦 Dependencies

All examples use the same dependencies as the main project:

```bash
# From project root
pip install -r requirements.txt
```

No additional dependencies required.

---

## 🧩 Code Reuse Philosophy

Examples follow DRY principles by:

1. **Importing from `utils/`** - No duplicate utility code
2. **Minimal data generation** - Simple, focused datasets
3. **Clear patterns** - Easy to adapt to your needs
4. **No over-engineering** - Just enough code to demonstrate

**Example:**
```python
# ❌ DON'T: Redefine plotting functions
def my_line_plot(df, x, y):
    # 20 lines of code...
    
# ✅ DO: Import from utils
from utils.plot_utils import line_plot

fig = line_plot(df, x='Date', y='Sales')
fig.show()
```

---

## 🎨 Customization

Each example is designed to be easily customizable:

```python
# Typical example structure:
# 1. Data loading/generation (EASY to replace)
df = pd.read_csv('data.csv')  # ← Replace with your data

# 2. Visualization (EASY to customize)
fig = line_plot(df, x='Date', y='Sales',  # ← Change parameters
                title='My Analysis')

# 3. Optional customization
fig.update_layout(height=600)  # ← Add your tweaks

# 4. Display
fig.show()
```

---

## 🤝 Contributing Examples

Have a useful Plotly pattern? Add it!

1. Choose the appropriate category (`01_quick_starts/`, `02_recipes/`, etc.)
2. Create a focused, minimal script
3. Add clear comments
4. Update this README
5. Submit a PR

**Guidelines:**
- ✅ Keep scripts under 100 lines
- ✅ Use existing utilities from `utils/`
- ✅ Include a docstring at the top
- ✅ Make data generation simple and clear
- ✅ Test that it runs standalone
- ❌ Don't duplicate notebook content
- ❌ Don't add new dependencies

---

## 📚 Related Resources

- **Full Tutorials**: See `docs/TUTORIALS.md`
- **API Reference**: See `docs/API.md`
- **Notebooks**: See `notebooks/` directory
- **Troubleshooting**: See `docs/TROUBLESHOOTING.md`

---

**Happy Plotting! 📊**
