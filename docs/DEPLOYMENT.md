# Deployment

## Local

```bash
make install-dev
make run-app        # Streamlit on http://localhost:8501
make run-jupyter    # JupyterLab on http://localhost:8888
```

Configuration is by environment variables (see `.env.example`):

| variable | effect |
|---|---|
| `PLOTLYVIZPRO_EXPORT_DIR` | root for `save_figure` and the legacy `save_fig_as_*` helpers (default `<project>/exports`) |
| `STREAMLIT_SERVER_PORT` | Streamlit port |

## Docker

```bash
docker compose up jupyter   # JupyterLab, :8888, notebooks/ and exports/ mounted
docker compose up app       # Streamlit gallery, :8501
```

The image is multi-stage (`python:3.12-slim`), installs `.[all]`, runs as a
non-root user and exposes a healthcheck that calls `plotlyvizpro info`.

Static images inside the container need Chrome for kaleido; add
`RUN kaleido_get_chrome` to the build stage if you export PNGs there.

## Streamlit Community Cloud

Point the app at `app.py`; set Python 3.12 and let it install from
`requirements.txt` (which resolves to `.[all]`). The bundled datasets and
manifest are committed, so no data step is required.

## GitHub Pages (docs)

`.github/workflows/docs.yml` builds MkDocs with `--strict` and deploys to the
`gh-pages` branch on every push to `main` that touches `docs/`, `mkdocs.yml`,
the package or the README. Enable Pages → "Deploy from branch: gh-pages" once.

## PyPI release

1. Bump `plotlyvizpro/_version.py`, update `docs/CHANGELOG.md` and `CITATION.cff`.
2. `git tag v2.1.0 && git push --tags`.
3. `.github/workflows/release.yml` builds sdist + wheel, creates a GitHub
   release with generated notes, and publishes via PyPI trusted publishing.
   Configure the `pypi` environment and the trusted publisher on PyPI first.
