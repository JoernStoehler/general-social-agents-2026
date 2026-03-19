"""Tests for metrics: KL divergence, total variation, log-likelihood."""

import math

import pytest

from src.metrics import kl_divergence, log_likelihood, total_variation


# --- Fixtures ---

@pytest.fixture
def uniform_3():
    """Uniform distribution over 3 actions."""
    return {1: 1 / 3, 2: 1 / 3, 3: 1 / 3}


@pytest.fixture
def peaked_3():
    """Distribution peaked on action 1."""
    return {1: 0.8, 2: 0.1, 3: 0.1}


@pytest.fixture
def dirac_3():
    """All mass on action 2."""
    return {1: 0.0, 2: 1.0, 3: 0.0}


# --- KL Divergence ---

class TestKLDivergence:

    def test_self_kl_is_zero(self, uniform_3):
        """KL(P || P) = 0 for any distribution."""
        kl = kl_divergence(uniform_3, uniform_3)
        assert kl == pytest.approx(0.0, abs=1e-8)

    def test_kl_nonnegative(self, uniform_3, peaked_3):
        """KL divergence is always >= 0."""
        assert kl_divergence(peaked_3, uniform_3) >= 0
        assert kl_divergence(uniform_3, peaked_3) >= 0

    def test_kl_asymmetric(self, uniform_3, peaked_3):
        """KL(P||Q) != KL(Q||P) in general."""
        kl_forward = kl_divergence(peaked_3, uniform_3)  # KL(uniform || peaked)
        kl_reverse = kl_divergence(uniform_3, peaked_3)  # KL(peaked || uniform)
        assert kl_forward != pytest.approx(kl_reverse, abs=0.01)

    def test_kl_known_value(self):
        """KL between two known distributions with manual computation."""
        # P = human = {1: 0.5, 2: 0.5}, Q = predicted = {1: 0.25, 2: 0.75}
        # KL(P||Q) = 0.5*ln(0.5/0.25) + 0.5*ln(0.5/0.75)
        #          = 0.5*ln(2) + 0.5*ln(2/3)
        human = {1: 0.5, 2: 0.5}
        predicted = {1: 0.25, 2: 0.75}
        expected = 0.5 * math.log(2) + 0.5 * math.log(2 / 3)
        kl = kl_divergence(predicted, human, laplace_alpha=0)
        assert kl == pytest.approx(expected, abs=1e-8)

    def test_kl_with_zero_human_entry(self):
        """If human(x)=0, that term contributes 0 to KL (by convention)."""
        human = {1: 0.0, 2: 1.0}
        predicted = {1: 0.5, 2: 0.5}
        # KL(human || predicted) = 0*log(0/0.5) + 1*log(1/0.5) = log(2)
        kl = kl_divergence(predicted, human, laplace_alpha=0)
        assert kl == pytest.approx(math.log(2), abs=1e-8)


# --- Total Variation ---

class TestTotalVariation:

    def test_self_tv_is_zero(self, uniform_3):
        """TV(P, P) = 0."""
        assert total_variation(uniform_3, uniform_3) == pytest.approx(0.0, abs=1e-10)

    def test_tv_symmetric(self, uniform_3, peaked_3):
        """TV is a metric: TV(P,Q) = TV(Q,P)."""
        tv1 = total_variation(peaked_3, uniform_3)
        tv2 = total_variation(uniform_3, peaked_3)
        assert tv1 == pytest.approx(tv2, abs=1e-10)

    def test_tv_between_zero_and_one(self, uniform_3, peaked_3, dirac_3):
        """TV is always in [0, 1]."""
        for p, q in [(uniform_3, peaked_3), (uniform_3, dirac_3), (peaked_3, dirac_3)]:
            tv = total_variation(p, q)
            assert 0 <= tv <= 1.0 + 1e-10

    def test_tv_known_value(self):
        """TV between disjoint distributions is 1."""
        p = {1: 1.0, 2: 0.0}
        q = {1: 0.0, 2: 1.0}
        assert total_variation(p, q) == pytest.approx(1.0, abs=1e-10)

    def test_tv_known_value_partial(self):
        """TV with known manual computation."""
        p = {1: 0.6, 2: 0.4}
        q = {1: 0.4, 2: 0.6}
        # TV = 0.5 * (|0.6-0.4| + |0.4-0.6|) = 0.5 * (0.2 + 0.2) = 0.2
        assert total_variation(p, q) == pytest.approx(0.2, abs=1e-10)


# --- Log-Likelihood ---

class TestLogLikelihood:

    def test_ll_perfect_match_is_maximum(self):
        """LL is maximized when predicted = human."""
        human = {1: 0.5, 2: 0.5}
        ll_match = log_likelihood(human, human, n=100, laplace_alpha=0)
        ll_worse = log_likelihood({1: 0.1, 2: 0.9}, human, n=100, laplace_alpha=0)
        assert ll_match > ll_worse

    def test_ll_is_negative(self):
        """Log-likelihood of any distribution is negative (probabilities < 1)."""
        human = {1: 0.3, 2: 0.7}
        predicted = {1: 0.5, 2: 0.5}
        ll = log_likelihood(predicted, human, n=100, laplace_alpha=0)
        assert ll < 0

    def test_ll_known_value(self):
        """Manual log-likelihood computation."""
        human = {1: 0.5, 2: 0.5}
        predicted = {1: 0.25, 2: 0.75}
        n = 100
        # counts: 50, 50
        # LL = 50*log(0.25) + 50*log(0.75)
        expected = 50 * math.log(0.25) + 50 * math.log(0.75)
        ll = log_likelihood(predicted, human, n=n, laplace_alpha=0)
        assert ll == pytest.approx(expected, abs=1e-8)

    def test_ll_scales_with_n(self):
        """LL scales linearly with n."""
        human = {1: 0.5, 2: 0.5}
        predicted = {1: 0.4, 2: 0.6}
        ll_100 = log_likelihood(predicted, human, n=100, laplace_alpha=0)
        ll_200 = log_likelihood(predicted, human, n=200, laplace_alpha=0)
        assert ll_200 == pytest.approx(2 * ll_100, abs=1e-8)
