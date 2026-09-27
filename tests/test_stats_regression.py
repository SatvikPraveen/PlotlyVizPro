"""OLS and LOWESS: closed-form checks and cross-validation against statsmodels."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from plotlyvizpro.stats import lowess, ols_fit
from tests.conftest import requires_statsmodels


class TestOLS:
    def test_recovers_exact_line(self):
        x = np.arange(10, dtype=float)
        y = 1.5 + 2.0 * x
        fit = ols_fit(x, y)
        assert fit.coef == pytest.approx([1.5, 2.0], abs=1e-9)
        assert fit.r_squared == pytest.approx(1.0)
        assert fit.residual_std == pytest.approx(0.0, abs=1e-9)
        assert fit.equation(2) == "y = 1.5 + 2x"

    def test_matches_closed_form_slope_intercept_and_stderr(self, linear_xy):
        x, y = linear_xy
        fit = ols_fit(x, y)
        n = x.size
        sxx = ((x - x.mean()) ** 2).sum()
        slope = ((x - x.mean()) * (y - y.mean())).sum() / sxx
        intercept = y.mean() - slope * x.mean()
        resid = y - (intercept + slope * x)
        s2 = (resid**2).sum() / (n - 2)
        assert fit.slope == pytest.approx(slope)
        assert fit.intercept == pytest.approx(intercept)
        assert fit.stderr[1] == pytest.approx(np.sqrt(s2 / sxx))
        assert fit.stderr[0] == pytest.approx(np.sqrt(s2 * (1 / n + x.mean() ** 2 / sxx)))
        assert fit.dof == n - 2
        assert fit.p_values[1] < 1e-10  # strong slope

    @requires_statsmodels
    @pytest.mark.statsmodels
    def test_matches_statsmodels_bands(self, linear_xy):
        import statsmodels.api as sm

        x, y = linear_xy
        fit = ols_fit(x, y, confidence=0.9)
        model = sm.OLS(y, sm.add_constant(x)).fit()
        frame = model.get_prediction(sm.add_constant(x)).summary_frame(alpha=0.1)
        np.testing.assert_allclose(fit.y_hat, frame["mean"].to_numpy(), rtol=1e-8)
        np.testing.assert_allclose(fit.ci_lower, frame["mean_ci_lower"].to_numpy(), rtol=1e-6)
        np.testing.assert_allclose(fit.ci_upper, frame["mean_ci_upper"].to_numpy(), rtol=1e-6)
        np.testing.assert_allclose(fit.pi_lower, frame["obs_ci_lower"].to_numpy(), rtol=1e-6)
        np.testing.assert_allclose(fit.pi_upper, frame["obs_ci_upper"].to_numpy(), rtol=1e-6)
        np.testing.assert_allclose(fit.p_values, model.pvalues, rtol=1e-6, atol=1e-12)
        assert fit.adj_r_squared == pytest.approx(model.rsquared_adj)

    @requires_statsmodels
    @pytest.mark.statsmodels
    def test_polynomial_matches_statsmodels(self):
        rs = np.random.default_rng(5)
        x = np.linspace(-3, 3, 120)
        y = 1 - 0.5 * x + 0.8 * x**2 + rs.normal(0, 0.5, x.size)
        fit = ols_fit(x, y, degree=2)
        import statsmodels.api as sm

        X = np.column_stack([np.ones_like(x), x, x**2])
        model = sm.OLS(y, X).fit()
        np.testing.assert_allclose(fit.coef, model.params, rtol=1e-6)
        np.testing.assert_allclose(fit.stderr, model.bse, rtol=1e-6)
        np.testing.assert_allclose(fit.y_hat, model.fittedvalues, rtol=1e-8)

    def test_datetime_x_is_preserved_for_display(self):
        dates = pd.date_range("2024-01-01", periods=30, freq="D")
        y = np.arange(30) * 2.0 + 5
        fit = ols_fit(pd.Series(dates), y)
        assert np.issubdtype(np.asarray(fit.x).dtype, np.datetime64)
        assert fit.r_squared == pytest.approx(1.0)
        assert fit.slope == pytest.approx(2.0)  # per day
        assert fit.x_unit == "day"
        assert "day" in fit.equation()

    def test_nan_rows_dropped(self):
        x = np.array([0, 1, 2, np.nan, 4, 5.0])
        y = np.array([0, 2, 4, 6, np.nan, 10.0])
        fit = ols_fit(x, y)
        assert fit.y_hat.size == 4
        assert fit.slope == pytest.approx(2.0)

    def test_ci_narrower_than_pi_and_widens_with_confidence(self, linear_xy):
        x, y = linear_xy
        f95 = ols_fit(x, y, confidence=0.95)
        f99 = ols_fit(x, y, confidence=0.99)
        assert np.all(f95.pi_upper - f95.pi_lower > f95.ci_upper - f95.ci_lower)
        assert np.all(f99.ci_upper - f99.ci_lower > f95.ci_upper - f95.ci_lower)

    def test_errors(self):
        with pytest.raises(ValueError, match="same length"):
            ols_fit([1, 2, 3], [1, 2])
        with pytest.raises(ValueError, match="finite observations"):
            ols_fit([1, 2], [1, 2])
        with pytest.raises(ValueError, match="confidence"):
            ols_fit([1, 2, 3], [1, 2, 3], confidence=1.0)
        with pytest.raises(ValueError, match="degree"):
            ols_fit([1, 2, 3], [1, 2, 3], degree=0)
        with pytest.raises(TypeError):
            ols_fit(["a", "b", "c"], [1, 2, 3])

    @settings(max_examples=25, deadline=None)
    @given(
        slope=st.floats(-50, 50),
        intercept=st.floats(-1e3, 1e3),
        n=st.integers(5, 60),
    )
    def test_property_exact_recovery(self, slope, intercept, n):
        x = np.linspace(0, 1, n)
        fit = ols_fit(x, intercept + slope * x)
        assert fit.slope == pytest.approx(slope, abs=1e-6, rel=1e-6)
        assert fit.intercept == pytest.approx(intercept, abs=1e-6, rel=1e-6)


class TestLowess:
    def test_recovers_linear_signal(self):
        x = np.linspace(0, 10, 100)
        y = 2 * x + 1
        fit = lowess(x, y, frac=0.5, iterations=0)
        np.testing.assert_allclose(fit.y_hat, y, atol=1e-8)

    @requires_statsmodels
    @pytest.mark.statsmodels
    def test_matches_statsmodels_lowess(self):
        from statsmodels.nonparametric.smoothers_lowess import lowess as sm_lowess

        rs = np.random.default_rng(3)
        x = np.sort(rs.uniform(0, 10, 150))
        y = np.sin(x) + rs.normal(0, 0.3, x.size)
        for it in (0, 3):
            ours = lowess(x, y, frac=0.3, iterations=it)
            ref = sm_lowess(y, x, frac=0.3, it=it, return_sorted=True)
            np.testing.assert_allclose(ours.y_hat, ref[:, 1], atol=2e-2)

    def test_robust_iterations_reduce_outlier_pull(self):
        x = np.linspace(0, 10, 80)
        y = np.sin(x)
        y[40] += 15  # one gross outlier
        plain = lowess(x, y, frac=0.3, iterations=0)
        robust = lowess(x, y, frac=0.3, iterations=3)
        assert abs(robust.y_hat[40] - np.sin(x[40])) < abs(plain.y_hat[40] - np.sin(x[40]))

    def test_delta_speedup_gives_similar_curve(self):
        rs = np.random.default_rng(1)
        x = np.linspace(0, 100, 2000)
        y = np.cos(x / 10) + rs.normal(0, 0.1, x.size)
        full = lowess(x, y, frac=0.1, iterations=1)
        fast = lowess(x, y, frac=0.1, iterations=1, delta=1.0)
        assert np.max(np.abs(full.y_hat - fast.y_hat)) < 0.05

    def test_sorted_output_and_datetime(self):
        dates = pd.Series(pd.date_range("2024-01-01", periods=20, freq="D"))[::-1].reset_index(drop=True)
        y = np.arange(20)[::-1]
        fit = lowess(dates, y, frac=0.5)
        assert np.all(np.diff(np.asarray(fit.x).astype("int64")) > 0)

    def test_errors(self):
        with pytest.raises(ValueError, match="frac"):
            lowess([1, 2, 3], [1, 2, 3], frac=0)
        with pytest.raises(ValueError, match="iterations"):
            lowess([1, 2, 3], [1, 2, 3], iterations=-1)
        with pytest.raises(ValueError, match="at least 3"):
            lowess([1, 2], [1, 2])
