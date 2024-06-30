import pytest
import numpy as np


class TestBase:

    @pytest.fixture
    def mock_latest_price(self):
        return {"SPY": 300, "AAPL": 350}

    @pytest.fixture
    def mock_total_price(self):
        return {
            "data": {"SPY": np.float64(600), "AAPL": np.float64(1400)},
            "total": np.float64(2000),
        }

    @pytest.fixture
    def mock_quantity_dict(self):
        return {"SPY": 2, "AAPL": 4}
