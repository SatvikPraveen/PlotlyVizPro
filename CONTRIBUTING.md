# 🤝 Contributing to PlotlyVizPro

Welcome to **PlotlyVizPro**! We're thrilled you're interested in contributing to this open-source visualization suite.

Whether you're here to fix bugs, enhance visualizations, refactor code, or improve documentation—your help is welcome!

---

## 📋 Table of Contents

- [👩‍💻 How to Contribute](#-how-to-contribute)
- [📦 Setting Up Locally](#-setting-up-locally)
- [📑 Project Structure](#-project-structure)
- [🎯 What You Can Work On](#-what-you-can-work-on)
- [🧪 Testing Guidelines](#-testing-guidelines)
- [💡 Style Guide](#-style-guide)
- [📢 Reporting Issues](#-reporting-issues)
- [🛡 Code of Conduct](#-code-of-conduct)

---

## 👩‍💻 How to Contribute

1. **Fork** the repository
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/PlotlyVizPro.git
   cd PlotlyVizPro
   ```

3. Create a new branch for your feature:

   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes 🚀
5. Commit and push:

   ```bash
   git commit -m "✨ Add [your feature/fix]"
   git push origin feature/your-feature-name
   ```
6. Open a **Pull Request** to the `main` branch.

---

## 📦 Setting Up Locally

Install the dependencies using a virtual environment or Docker:

### Option 1: Using `venv`

```bash
python -m venv plotly_env
source plotly_env/bin/activate
pip install -r requirements.txt
```

### Option 2: Using Docker

```bash
docker build -t plotlyvizpro-jupyter .
docker run -d -p 8890:8888 -v $(pwd):/app --name plotlyvizpro plotlyvizpro-jupyter
```

Access JupyterLab at: `http://localhost:8890`

---

## 📑 Project Structure

```bash
PlotlyVizPro/
├── exports/               # Saved figures (html/png)   
├── notebooks/             # Jupyter notebooks (modular)   
├── pages/                 # Streamlit app pages   
├── utils/                 # Reusable plotting & data functions
├── .dockerignore             
├── .gitignore                
├── app.py                    
├── CODE_OF_CONDUCT.md        
├── CONTRIBUTING.md           
├── Dockerfile                
├── generate_datasets.py      
├── LICENSE                   
├── README.md                 
└── requirements.txt

```

---

## 🎯 What You Can Work On

✅ Add new visualization notebooks
✅ Improve existing charts with better interactivity
✅ Refactor utilities into reusable modules
✅ Add unit tests for custom utility functions
✅ Create Streamlit dashboards from notebooks
✅ Enhance README, add examples or usage guides
✅ Fix bugs or improve layout/styling of charts

---

## 🧪 Testing Guidelines

* Prefer using `pytest` for testing utility functions.
* Use `assert` statements inside notebooks for sanity checks.
* Validate exported plots (HTML, PNG) are correctly generated and saved in `/exports`.

---

## 💡 Style Guide

* Follow [PEP8](https://peps.python.org/pep-0008/) for code formatting.
* Use meaningful variable and function names.
* Write docstrings for all functions in `utils/`.
* Avoid hardcoding paths—use `Pathlib` when possible.

---

## 📢 Reporting Issues

Found a bug or have a suggestion?

1. Open an [Issue](https://github.com/SatvikPraveen/PlotlyVizPro/issues)
2. Use clear, descriptive titles and screenshots if relevant.
3. Mention relevant notebook filenames or lines if applicable.

---

## 🛡 Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/) to ensure a welcoming community for all.

---

Thank you for being a part of this project!
— The PlotlyVizPro Team 🚀
