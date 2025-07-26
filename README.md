# 📊 PlotlyVizPro – Mastering Interactive Visualizations with Plotly

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-darkgreen.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Plotly](https://img.shields.io/badge/Plotly-100%25-brightgreen.svg)](https://plotly.com/python/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blueviolet.svg)](https://www.docker.com/)

---

## 📦 Overview

**PlotlyVizPro** is a modular, multi-notebook visualization project crafted to help you master interactive plotting using **Plotly**, **Streamlit**, and **Python utilities**. From chart fundamentals to advanced dashboards, this project equips you with:

✅ A reusable, utility-first visualization toolkit  
✅ A thematic, notebook-driven learning framework  
✅ A polished, production-grade portfolio project

---

## 🚀 Highlights

- 📈 **Express + Graph Objects**: Built using both Plotly APIs
- 📊 **Charts**: Line, bar, pie, box, histogram, heatmap, KDE
- 🧭 **Maps**: Choropleth, Mapbox, GeoJSON overlays
- 🧮 **Statistical Add-ons**: Trendlines, Z-bands, moving averages
- 🔄 **Animations**: Sliders, dropdown filters, `animation_frame`
- 🧼 **Clean Output**: HTML for interactivity, PNG for documentation
- 🧰 **Modular Design**: Plotting utilities, reusable layout functions
- 🐳 **Docker Support**: Containerized Jupyter environment for reproducibility

---

## 🧠 Core Concepts Covered

| Area               | Concepts                                                           |
| ------------------ | ------------------------------------------------------------------ |
| Basic Charts       | Line, scatter, bar, pie, histogram, box plots                      |
| Chart Styling      | Theming, axis config, layout tuning, custom tooltips               |
| Interactivity      | Hover templates, sliders, dropdowns, callbacks                     |
| Statistical Layers | Trendlines, rolling averages, ±z-score confidence bands            |
| Dashboard Design   | Subplots, grids, shared axes, spacings, annotations                |
| Geo Visuals        | Choropleths, GeoJSON overlays, Mapbox tokens                       |
| Plot Architecture  | `.pipe()` overlays, centralized `plot_utils.py`, layout automation |
| Exports            | Dynamic HTML and static PNG renderings for reporting               |

---

## 🗂️ Project Structure

```bash
PlotlyVizPro/
├── exports/                  # HTML and PNG exports by notebook
├── notebooks/                # 10 structured Jupyter notebooks
├── pages/                    # Streamlit pages for app mode
├── utils/                    # Reusable plotting utilities
├── cheatsheets/             # Markdown-based syntax guides
├── .gitignore                # Ignores env folders, checkpoints, etc.
├── Dockerfile                # Docker environment for reproducibility
├── app.py                    # Main Streamlit app entry point
├── generate_datasets.py      # Generates synthetic datasets using Faker
├── requirements.txt          # Python dependencies
├── README.md                 # You’re here!
```

---

## 📓 Notebooks Overview

| #   | Notebook Title                 | Concepts & Charts                            |
| --- | ------------------------------ | -------------------------------------------- |
| 01  | Line & Scatter Charts          | Line, scatter, bubble, tooltips, color maps  |
| 02  | Bar, Pie & Box Charts          | Categorical visualizations                   |
| 03  | Histogram, KDE & Heatmaps      | Distribution plots, hexbin overlays          |
| 04  | Choropleth & GeoJSON Maps      | Choropleth, projections, custom shape tuning |
| 05  | Animation & Interactivity      | Sliders, dropdowns, animation_frame          |
| 06  | Dashboards & Subplots          | Grid layouts, spacing, multi-panel views     |
| 07  | Graph Objects Deep Dive        | Manual axis, layout, annotation control      |
| 08  | Mapbox & Geo Layers            | Mapbox tokens, styles, satellite maps        |
| 09  | Real-World Visualizations      | COVID & Superstore use cases                 |
| 10  | Statistical Overlays + .pipe() | Modular overlays, Z-bands, moving average    |

---

## ⚙️ Setup Instructions

### ▶️ Local Setup

```bash
# Clone the repo
git clone https://github.com/SatvikPraveen/PlotlyVizPro.git
cd PlotlyVizPro

# Create a virtual environment
python3 -m venv plotly_env
source plotly_env/bin/activate  # On Windows: plotly_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch JupyterLab
jupyter lab
```

---

## 🐳 Docker Setup (Optional)

```bash
# Build image
docker build -t plotlyvizpro .

# Run container (auto-launches JupyterLab at port 8888)
docker run -p 8888:8888 plotlyvizpro
```

🛡️ No token/password required. Uses `--allow-root` for compatibility.

---

## 🧪 Datasets

All datasets are **synthetically generated** via `generate_datasets.py` using the `faker` library.

- 🔁 Fully reproducible
- 🔓 License-free
- 🔬 Customizable complexity (sales, dates, geography, etc.)

---

## 🧰 Utility Functions (utils/plot_utils.py)

| Type          | Utilities                                                      |
| ------------- | -------------------------------------------------------------- |
| Core Charts   | `line_plot()`, `bar_plot()`, `scatter_plot()`, `box_plot()`    |
| Interactivity | Sliders, hover templates, dropdowns                            |
| Stats Add-ons | `add_trendline()`, `add_moving_average()`, `add_zscore_band()` |
| Layout Tools  | `make_subplots_custom()`, `add_annotations()`, `apply_theme()` |
| Export Tools  | `save_fig_as_html()`, `save_fig_as_png()`                      |

---

## 📤 Plot Exports

Each notebook saves plots in:

```bash
exports/
├── html/             # Interactive outputs
│   ├── 01_line_scatter/
│   ├── ...
├── images/           # PNG renders
│   ├── 01_line_scatter/
│   ├── ...
```

---

## 📌 Cheatsheet

A compact markdown cheatsheet available at:

```bash
cheatsheets/plotly_cheatsheet.md
```

Includes:

- Plotly syntax patterns
- Utility usage demos
- Dashboard tips
- Export best practices

---

## 📜 License

Licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## 🤝 Contributions Welcome

- 🛠 Got a bug fix or improvement? [Open a PR](https://github.com/SatvikPraveen/PlotlyVizPro/pulls)
- 🧠 Found a bug or want to request a feature? [File an issue](https://github.com/SatvikPraveen/PlotlyVizPro/issues)
- ⭐ If this helped you, consider starring the repository!

---

## 🧭 Related Projects

Explore the full suite of Python data mastery repositories:

- 📊 [**PandasPlayground**](https://github.com/SatvikPraveen/PandasPlayground)  
  Modular pipelines for mastering data wrangling, merging, and analysis using pandas.

- 🔢 [**NumPyMasterPro**](https://github.com/SatvikPraveen/NumPyMasterPro)  
  A concept-to-implementation NumPy project covering arrays, broadcasting, and indexing.

- 📈 [**MatplotlibMasterPro**](https://github.com/SatvikPraveen/MatplotlibMasterPro)  
  Comprehensive Matplotlib practice with style guides, animations, and thematic plots.

- 🖼️ [**SeabornMasterPro**](https://github.com/SatvikPraveen/SeabornMasterPro)  
  Complete mastery of Seaborn's statistical plots, themes, dashboards, and time series.

Each project is standalone but follows a consistent **pedagogical and modular structure**, forming a **progressive learning track** in data visualization and numerical computing with Python.

---
