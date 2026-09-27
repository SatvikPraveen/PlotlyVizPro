## Summary

<!-- What changes and why. Link issues with "Closes #123". -->

## Type

- [ ] Bug fix
- [ ] New estimator / overlay / chart
- [ ] Docs
- [ ] CI / tooling
- [ ] Breaking change (explain the migration)

## Checklist

- [ ] `make check` passes locally (ruff, mypy --strict, pytest with coverage gate)
- [ ] New numerical code has a closed-form or reference-implementation test
- [ ] Public functions have numpy-style docstrings; new modules are listed under `docs/api/`
- [ ] `docs/CHANGELOG.md` updated
- [ ] If datasets were regenerated: manifest and exports updated, and it is called out below
- [ ] Notebooks / Streamlit pages touched were executed (`make test-notebooks`, AppTest)

## Notes for reviewers

<!-- Screenshots of figures, numerical comparisons, or anything non-obvious. -->
