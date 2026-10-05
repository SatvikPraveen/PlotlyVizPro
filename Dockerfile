# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Build layer: install the package with runtime + notebook extras.
FROM base AS build
COPY pyproject.toml README.md LICENSE ./
COPY plotlyvizpro ./plotlyvizpro
RUN pip install --upgrade pip && pip install --prefix=/install ".[all]"

# Runtime layer: copy the installed prefix (version-agnostic), run as a non-root user.
FROM base AS runtime
COPY --from=build /install /usr/local
COPY . .
RUN useradd --create-home --uid 1000 viz && chown -R viz:viz /app
USER viz

EXPOSE 8888 8501

HEALTHCHECK --interval=30s --timeout=5s CMD plotlyvizpro info > /dev/null || exit 1

# Default: JupyterLab. Override with `streamlit run app.py` for the gallery.
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.token=", "--ServerApp.password="]
