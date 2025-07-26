# 📊 PlotlyVizPro – Mastering Interactive Visualizations with Plotly

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-darkgreen.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Plotly](https://img.shields.io/badge/Plotly-100%25-brightgreen.svg)](https://plotly.com/python/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blueviolet.svg)](https://www.docker.com/)

---

## 📦 Overview

**PlotlyVizPro** is a modular, real-world data visualization project designed to help you **master Plotly** from first principles to production-grade dashboards. This project doubles as:

✅ A personal learning repository
✅ A reusable utility-driven toolkit
✅ A professional portfolio showcase

---

## 🚀 Highlights

- 📈 **Plotly Express & Graph Objects**
- 📊 **Bar, Line, Pie, Box, Histogram, Heatmap, KDE**
- 🗺️ **Choropleth, GeoJSON, and Mapbox maps**
- 🔄 **Animated visualizations & interactive controls**
- 🔧 **Statistical overlays: trendlines, moving averages, Z-score bands**
- 🧰 **Utility-first design with modular plotting functions**
- 🧼 **Clean exports: HTML for interactivity, PNG for reporting**

---

## 🧠 Core Concepts Covered

| Topic              | Features                                                                |
| ------------------ | ----------------------------------------------------------------------- |
| Basic Charts       | Line, scatter, bar, pie, box, histogram                                 |
| Advanced Styling   | Layout tuning, themes, axis control, annotations                        |
| Interactivity      | Dropdown menus, sliders, animation_frame, hover templates               |
| Dashboards         | Subplots, multi-panel grid layouts, shared axes                         |
| Geo Visualization  | Choropleth maps, Mapbox integration, city-level data with custom tokens |
| Statistical Layers | Linear trendlines, rolling averages, ±z-score confidence bands          |
| Reusability        | `.pipe()`-style modular overlays, centralized utility functions         |

---

## 🗂️ Project Structure

```bash
PlotlyVizPro/
├── datasets/                # Synthetic datasets for demos & case studies
├── notebooks/               # 10 Jupyter notebooks (thematic, advanced)
├── utils/                   # Reusable plotting functions (plot_utils.py)
├── exports/
│   ├── html/                # Interactive HTML exports by notebook
│   └── images/              # Static PNG snapshots by notebook
├── cheatsheets/            # Markdown summary of all utilities & patterns
├── generate_datasets.py    # Script to generate synthetic data reproducibly
├── requirements.txt        # Virtual environment dependencies
└── README.md               # You’re here!
```

---

## 📓 Notebooks Overview

| 🧾 No. | Notebook Title                    | Key Visualizations & Concepts                   |
| ------ | --------------------------------- | ----------------------------------------------- |
| 01     | Line & Scatter Charts             | Line, scatter, bubble, styling & tooltips       |
| 02     | Bar, Pie & Box Charts             | Categorical distribution plots                  |
| 03     | Histogram, Density, Heatmaps      | KDE, correlation heatmaps, hexbin overlays      |
| 04     | Geo & Choropleth Maps             | Choropleth, GeoJSON overlays, projection tuning |
| 05     | Animations & Interactive Controls | Sliders, dropdowns, `animation_frame`, filters  |
| 06     | Subplots & Dashboards             | GridSpec-style dashboards, shared axes, spacing |
| 07     | Graph Objects Deep Dive           | Fine control: annotations, shapes, updates      |
| 08     | Mapbox with Styles & Layers       | Custom Mapbox tokens, city & satellite views    |
| 09     | Real-World Visualizations         | Superstore sales dashboard, COVID-19 choropleth |
| 10     | Statistical Overlays & .pipe()    | Trendlines, rolling avg, Z-bands, modular plots |

---

## ⚙️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/SatvikPraveen/PlotlyVizPro.git
cd PlotlyVizPro

# Create virtual environment
python3 -m venv plotly_env
source plotly_env/bin/activate      # On Windows: plotly_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter and start exploring notebooks/
```

---

## 🧪 Datasets

All datasets are **artificially generated** using `generate_datasets.py`. This ensures:

- 💯 No data license restrictions
- 🔁 Full reproducibility
- 🧪 Controlled complexity for targeted visualizations

---

## 🧰 Utilities Overview

The `utils/plot_utils.py` module contains:

| Category          | Utilities                                                      |
| ----------------- | -------------------------------------------------------------- |
| Basic Charts      | `line_plot()`, `bar_plot()`, `scatter_plot()`, `box_plot()`    |
| Statistical Tools | `add_trendline()`, `add_moving_average()`, `add_zscore_band()` |
| Layout Helpers    | `make_subplots_custom()`, `apply_theme()`, `add_annotations()` |
| Exporters         | `save_fig_as_html()`, `save_fig_as_png()`                      |
| Dashboard Extras  | Subplot spacing, shared axes, annotation layers                |
| Interactivity     | Sliders, dropdowns, hover tweaks                               |

---

## 📤 Exports

Each notebook saves plots in two formats:

- **HTML** → Fully interactive Plotly charts
- **PNG** → Static, high-quality images

Output directories:

```bash
exports/
├── html/
│   ├── 01_line_scatter/
│   ├── ...
├── images/
│   ├── 01_line_scatter/
│   ├── ...
```

---

## 🧵 Cheatsheet

Find a concise **Plotly + project-specific cheatsheet** in:

```
cheatsheets/plotly_cheatsheet.md
```

Includes:

- Syntax patterns
- Thematic chart groups
- Utility usage examples
- Export best practices

---

## 🐳 Optional: Run in Docker

Build and launch a containerized Jupyter environment with all dependencies:

```bash
# (Coming Soon)
docker build -t plotlyvizpro .
docker run -p 8888:8888 plotlyvizpro
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 💬 Feedback & Contributions

- 💡 Found something useful? Give it a ⭐
- 🛠 Found an issue or want to suggest an improvement? [Open an issue](https://github.com/SatvikPraveen/PlotlyVizPro/issues)
- 🤝 Pull requests welcome!

---
