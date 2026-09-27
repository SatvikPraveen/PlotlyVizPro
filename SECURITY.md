# Security policy

## Supported versions

| Version | Supported |
|---|---|
| 2.x | yes |
| 1.x | no |

## Reporting a vulnerability

Please do not open a public issue for security problems. Use GitHub's
private vulnerability reporting on this repository ("Security" tab →
"Report a vulnerability"). You will get an acknowledgement within a week.

## Scope notes

- The library performs no network access. `save_html(include_plotlyjs="cdn")`
  produces HTML that loads Plotly from `cdn.plot.ly` when opened; pass
  `include_plotlyjs=True` for fully offline files.
- `provenance.git_commit` shells out to `git` in the working directory only.
- The Streamlit palette page renders user-supplied hex strings into inline
  styles after validating them as 3- or 6-digit hex.
