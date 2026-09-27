# Methods

This page states exactly what each estimator computes, with the formulas and
references the tests are written against.

## Ordinary least squares (`stats.regression.ols_fit`)

For a polynomial of degree \(d\) the design matrix is \(X = [1, z, z^2, \dots, z^d]\)
with \(z = (x - \bar x)/s_x\) for conditioning. Coefficients are solved by QR
decomposition. With \(n\) observations, \(p = d + 1\) parameters, residual
degrees of freedom \(\nu = n - p\), residual variance
\(s^2 = \mathbf r^\top \mathbf r / \nu\) and leverage
\(h_i = \mathbf x_i^\top (X^\top X)^{-1} \mathbf x_i\):

\[
\text{CI}_i = \hat y_i \pm t_{\alpha/2,\,\nu}\; s \sqrt{h_i},
\qquad
\text{PI}_i = \hat y_i \pm t_{\alpha/2,\,\nu}\; s \sqrt{1 + h_i}.
\]

Coefficients are mapped back to the original x scale through the binomial
expansion Jacobian, and their standard errors from the transformed covariance
\(J\,(s^2 (X^\top X)^{-1})\,J^\top\). Two-sided p-values use the *t*
distribution with \(\nu\) degrees of freedom. Datetime x is expressed in days
since the first observation, so a slope reads "units per day".

*Verified against* `statsmodels.OLS.get_prediction().summary_frame()` (mean
and observation intervals, rtol 1e-6) and `params`, `bse`, `pvalues`,
`rsquared_adj` for degrees 1 and 2.

## LOWESS (`stats.regression.lowess`)

Cleveland (1979). For each \(x_i\) the \(k = \lceil f\,n \rceil\) nearest
points get tricube weights \(w_j = (1 - (|x_j - x_i|/h_i)^3)^3\), a weighted
linear fit is evaluated at \(x_i\), and (for `iterations > 0`) residuals are
re-weighted with the bisquare function \(B(u) = (1-u^2)^2\) for
\(|u| = |r|/(6\,\mathrm{MAD}) < 1\). The optional `delta` skips local fits for
points closer than `delta` to the last fit and interpolates linearly.

*Verified against* `statsmodels.nonparametric.lowess` for 0 and 3 robustifying
iterations (atol 0.02 on a noisy sine).

## Bootstrap (`stats.bootstrap.bootstrap_ci`)

\(B\) resamples with replacement; \(\hat\theta^*_b\) is the statistic on each.

- **percentile**: \([\hat\theta^*_{(\alpha/2)},\ \hat\theta^*_{(1-\alpha/2)}]\).
- **basic**: \([2\hat\theta - \hat\theta^*_{(1-\alpha/2)},\ 2\hat\theta - \hat\theta^*_{(\alpha/2)}]\).
- **BCa** (default): bias correction \(z_0 = \Phi^{-1}(\#\{\hat\theta^*_b < \hat\theta\}/B)\),
  acceleration from the jackknife
  \(a = \sum (\bar\theta_{(\cdot)} - \hat\theta_{(i)})^3 \big/ 6\big[\sum (\bar\theta_{(\cdot)} - \hat\theta_{(i)})^2\big]^{3/2}\),
  adjusted quantiles
  \(\alpha_k = \Phi\!\left(z_0 + \frac{z_0 + z_{k}}{1 - a(z_0 + z_{k})}\right)\).

Efron & Tibshirani (1993), ch. 14. Tests check reproducibility with a seed,
asymmetry on log-normal data, degenerate fallback, and empirical coverage of
the percentile interval on \(N(0,1)\), \(n = 30\) (200 trials, 90-99 % band).

## Anomaly detection (`stats.anomaly`)

| Detector | Rule | Notes |
|---|---|---|
| `zscore_outliers` | \(|y - c| / s > \tau\) with \(c, s\) = mean, SD (or median, \(1.4826\,\mathrm{MAD}\) when `robust`) | global; masking-prone unless robust |
| `iqr_outliers` | outside \([Q_1 - k\,\mathrm{IQR},\ Q_3 + k\,\mathrm{IQR}]\) | Tukey's fences, distribution-free |
| `hampel_filter` | \(|y_i - \tilde y_i| > n_\sigma \cdot 1.4826\,\mathrm{MAD}_i\) over a centred window of \(2w+1\) | local; handles drift and trend |
| `generalized_esd` | Rosner (1983): remove the most extreme point \(i = 1..r\), compare \(R_i\) with \(\lambda_i = \frac{(n-i)\,t_{p,n-i-1}}{\sqrt{(n-i-1+t^2_{p,n-i-1})(n-i+1)}}\), \(p = 1 - \frac{\alpha}{2(n-i+1)}\); the outlier count is the largest \(i\) with \(R_i > \lambda_i\) | *verified against* the NIST/SEMATECH e-Handbook §1.3.5.17.3 example (3 outliers) |

## Distributions (`stats.distributions`)

- **KDE**: Gaussian kernel via `scipy.stats.gaussian_kde`; bandwidth by
  Scott's or Silverman's rule or a numeric factor. Integrates to 1 on the
  returned grid (checked to 0.01).
- **ECDF**: \(\hat F(x_{(i)}) = i/n\). Optional simultaneous band from the
  Dvoretzky-Kiefer-Wolfowitz inequality with Massart's constant:
  \(\varepsilon = \sqrt{\ln(2/\alpha) / (2n)}\).
- **Q-Q**: `scipy.stats.probplot` quantiles and least-squares reference line;
  \(R^2\) reported.
- **Bin rules**: `numpy.histogram_bin_edges` (`fd` default).

## Seasonal decomposition (`stats.decomposition.seasonal_decompose`)

Classical moving-average decomposition (Hyndman & Athanasopoulos, FPP §3.4).
Trend: centred \(m\)-MA for odd \(m\), \(2\times m\)-MA for even \(m\).
Seasonal: period-wise means of the detrended series, normalised to sum to 0
(additive) or average 1 (multiplicative). Strength measures
\(F_S = \max(0,\ 1 - \mathrm{Var}(R)/\mathrm{Var}(S + R))\) and
\(F_T\) analogously (Wang, Smith & Hyndman 2006).

*Verified against* `statsmodels.tsa.seasonal.seasonal_decompose` for periods
7 and 12, additive and multiplicative (rtol 1e-6).

## Colour (`colors`)

- sRGB → linear → OKLab uses Ottosson's (2020) matrices; OKLCH lightness
  \(L\), chroma \(C = \sqrt{a^2 + b^2}\), hue \(\operatorname{atan2}(b, a)\).
- CVD simulation applies the Machado, Oliveira & Fernandes (2009) severity-1.0
  matrices in linear RGB, then clips and re-encodes.
- \(\Delta E = 100\,\lVert \mathrm{OKLab}_1 - \mathrm{OKLab}_2 \rVert_2\).
- Contrast is the WCAG 2.x ratio \((L_1 + 0.05)/(L_2 + 0.05)\) on relative luminance.

The audit checks (per mode) are: lightness band (light 0.43-0.77, dark
0.48-0.67), chroma \(\ge 0.10\), CVD separation on the pair list
(\(\ge 8\) pass, 6-8 warn, \(< 6\) fail, using \(\min\) of protan and deutan),
normal-vision floor (\(\ge 15\), hard gate), and contrast vs surface
(\(\ge 3{:}1\), otherwise a warning that requires direct labels or a table
view). `order_palette` maximises the minimum adjacent CVD \(\Delta E\)
exhaustively for \(\le 8\) colours and greedily beyond.

## Downsampling (`downsample`)

- **LTTB** (Steinarsson 2013): first and last points fixed; the interior is
  split into \(t-2\) buckets; in each bucket the point maximising the area of
  the triangle with the previously selected point and the next bucket's mean is
  kept. Vectorised per bucket, O(n).
- **MinMax**: per-bucket argmin and argmax, giving an exact envelope.
- **M4** (Jugel et al. 2014): first, last, min, max per pixel column, columns
  defined by x range so gaps are respected; pixel-exact for line rendering at
  that width.
- `max_error` reports the largest vertical distance between the original
  series and the linear interpolant through the kept points.

Property tests (Hypothesis) assert endpoint retention, monotone indices and
sizes for random inputs; a hand-checked 7-point case pins LTTB's bucket choice.
