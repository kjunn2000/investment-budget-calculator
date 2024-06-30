from engine_lambda.main import (
    _extract_ticket,
    _extract_tickets,
    _calculate_latest_price,
)
import pandas as pd
from test_base import TestBase


class TestAggregratePrice(TestBase):

    def test_extract_ticket(self):
        data = {
            "Close": pd.Series(
                [100, 200, 300], index=["2023-01-01", "2023-01-02", "2023-01-03"]
            )
        }
        market_data = pd.DataFrame(data)
        ticket = "SPY"
        expected = {ticket: 300}

        result = _extract_ticket(market_data, ticket)

        assert result == expected

    def test_extract_tickets(self, mock_latest_price):
        market_data = pd.DataFrame(
            {"SPY": [100, 200, 300], "AAPL": [150, 250, 350]},
            index=["2023-01-01", "2023-01-02", "2023-01-03"],
        )
        tickets = ["SPY", "AAPL"]
        expected = mock_latest_price
        wrapped_market_data = {"Close": market_data}

        result = _extract_tickets(wrapped_market_data, tickets)

        assert result == expected

    def test_calculate_price(
        self, mock_latest_price, mock_quantity_dict, mock_total_price
    ):
        response = _calculate_latest_price(mock_latest_price, mock_quantity_dict)

        assert response == mock_total_price