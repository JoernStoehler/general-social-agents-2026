"""Tests for baselines: Nash equilibrium, level-k, uniform."""

import pytest

from src.baselines import (
    level_k_distribution,
    nash_equilibrium_computed,
    nash_equilibrium_symmetric,
    uniform_distribution,
)
from src.games import ELEVEN_TWENTY_GAME


game = ELEVEN_TWENTY_GAME


class TestNashEquilibrium:

    def test_nash_symmetric_sums_to_one(self):
        nash = nash_equilibrium_symmetric(game)
        assert sum(nash.values()) == pytest.approx(1.0, abs=1e-10)

    def test_nash_symmetric_support(self):
        """Nash support is {15, 16, 17, 18, 19, 20}, zero elsewhere."""
        nash = nash_equilibrium_symmetric(game)
        for a in range(11, 15):
            assert nash[a] == 0.0
        for a in range(15, 21):
            assert nash[a] > 0.0

    def test_nash_symmetric_known_values(self):
        nash = nash_equilibrium_symmetric(game)
        assert nash[15] == pytest.approx(0.25, abs=1e-10)
        assert nash[16] == pytest.approx(0.25, abs=1e-10)
        assert nash[17] == pytest.approx(0.20, abs=1e-10)
        assert nash[18] == pytest.approx(0.15, abs=1e-10)
        assert nash[19] == pytest.approx(0.10, abs=1e-10)
        assert nash[20] == pytest.approx(0.05, abs=1e-10)

    def test_nash_computed_matches_analytic(self):
        analytic = nash_equilibrium_symmetric(game)
        computed = nash_equilibrium_computed(game)
        for a in game.action_space:
            assert computed[a] == pytest.approx(analytic[a], abs=1e-4)


class TestLevelK:

    def test_level_0_is_uniform(self):
        l0 = level_k_distribution(game, 0)
        for a in game.action_space:
            assert l0[a] == pytest.approx(0.1, abs=1e-10)

    def test_level_1_is_19(self):
        l1 = level_k_distribution(game, 1)
        assert l1[19] == 1.0
        assert all(l1[a] == 0.0 for a in game.action_space if a != 19)

    def test_level_2_is_18(self):
        l2 = level_k_distribution(game, 2)
        assert l2[18] == 1.0

    def test_level_3_is_17(self):
        l3 = level_k_distribution(game, 3)
        assert l3[17] == 1.0

    def test_level_k_sums_to_one(self):
        for k in range(5):
            lk = level_k_distribution(game, k)
            assert sum(lk.values()) == pytest.approx(1.0, abs=1e-10)


class TestUniform:

    def test_uniform_sums_to_one(self):
        u = uniform_distribution(game)
        assert sum(u.values()) == pytest.approx(1.0, abs=1e-10)

    def test_uniform_is_equal(self):
        u = uniform_distribution(game)
        for a in game.action_space:
            assert u[a] == pytest.approx(0.1, abs=1e-10)
