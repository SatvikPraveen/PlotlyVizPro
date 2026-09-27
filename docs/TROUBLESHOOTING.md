# Troubleshooting

**`RuntimeError: Static image export requires the 'kaleido' package`**
`pip install kaleido`, then run `kaleido_get_chrome` if no Chrome/Chromium is
installed. `plotlyvizpro info` reports whether the engine is available.

**`TypeError: write_image() got an unexpected keyword argument 'engine'`**
You are calling Plotly directly with the pre-6.0 signature. Use
`plotlyvizpro.export.save_image`, which is version-agnostic.

**`IntegrityError: superstore.csv: sha256 … does not match manifest`**
A dataset was edited by hand. Either regenerate (`plotlyvizpro generate-data`)
or, if the change is intended, rewrite the manifest with
`plotlyvizpro.data.write_manifest()`. Pass `verify=False` to `load` to bypass.

**`KeyError: Column(s) ['Sale'] not found. Available: [...]`**
Chart builders validate column names up front; check spelling and case.

**`ValueError: x must be sorted in non-decreasing order`**
Downsamplers need ordered x. Sort first: `order = np.argsort(x); x, y = x[order], y[order]`.

**LOWESS is slow**
Complexity is O(n · k). Pass `delta` (in x units) so nearby points reuse
interpolation, or downsample first.

**Palette audit says WARN on contrast**
Colours below 3:1 against the surface are allowed only with direct labels or a
table view. Use `sequential_scale` for magnitude encodings instead of forcing
a categorical colour darker.

**Notebooks cannot import `plot_utils`**
Run them from `notebooks/` (they insert `../utils` into `sys.path`) or install
the package (`pip install -e .`), which makes the facade importable anywhere.

**`NoSuchKernel: No such kernel named python3` when executing notebooks**
`pip install ipykernel` in the same environment (included in the `notebooks` extra).

**Streamlit shows a stale chart after editing a page**
Cached dataset loads are keyed by name; press `C` then `R` in the app to clear
caches, or restart `streamlit run`.

**mypy complains about pandas types in my code**
Install `pandas-stubs` (in the `dev` extra); the package itself is `--strict` clean.
