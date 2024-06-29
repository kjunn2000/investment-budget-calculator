from numpy import float64
from engine_lambda.main import (
    _download_tickets,
    _extract_ticket,
    _extract_tickets,
    _calculate_latest_price,
    handler,
)
import numpy as np
from unittest.mock import ANY
import pandas as pd

mock_latest_price = {"SPY": 300, "AAPL": 350}

mock_total_price = {"SPY": np.float64(600), "AAPL": np.float64(1400)}

mock_quantity_dict = {"SPY": 2, "AAPL": 4}


class TestDownloadTicket:

    def test_download_one_ticket(self, mocker):
        input_ticket_numbers = ["SPY"]
        mocker.patch("engine_lambda.main.yf.download")
        mock_extract_ticket = mocker.patch(
            "engine_lambda.main._extract_ticket", return_value={"SPY": np.float64(300)}
        )

        response = _download_tickets(input_ticket_numbers)

        assert response is not None
        assert type(response["SPY"]) == float64
        mock_extract_ticket.assert_called_once_with(ANY, "SPY")

    def test_download_multiple_tickes(self, mocker):
        input_ticket_numbers = ["SPY", "NVDA"]
        mocker.patch("engine_lambda.main.yf.download")

        mock_extract_tickets = mocker.patch(
            "engine_lambda.main._extract_tickets",
            return_value={"SPY": np.float64(300), "NVDA": np.float64(300)},
        )

        response = _download_tickets(input_ticket_numbers)

        assert response is not None
        assert type(response["SPY"]) == float64
        assert type(response["NVDA"]) == float64
        mock_extract_tickets.assert_called_once_with(ANY, input_ticket_numbers)

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

    def test_extract_tickets(self):
        market_data = pd.DataFrame(
            {"SPY": [100, 200, 300], "AAPL": [150, 250, 350]},
            index=["2023-01-01", "2023-01-02", "2023-01-03"],
        )
        tickets = ["SPY", "AAPL"]
        expected = mock_latest_price
        wrapped_market_data = {"Close": market_data}

        result = _extract_tickets(wrapped_market_data, tickets)

        assert result == expected

    def test_calculate_price(self):
        response = _calculate_latest_price(mock_latest_price, mock_quantity_dict)

        assert response == mock_total_price

    def test_handler_with_one_ticket(self, mocker):
        event = {"body": {"SPY": 2, "AAPL": 4}}
        mock_download = mocker.patch(
            "engine_lambda.main._download_tickets", return_value=mock_latest_price
        )
        mock_calculate_price = mocker.patch(
            "engine_lambda.main._calculate_latest_price", return_value=mock_total_price
        )

        response = handler(event, {})

        mock_download.assert_called_once_with(event.get("body").keys())
        mock_calculate_price.assert_called_once_with(
            mock_latest_price, mock_quantity_dict
        )
        assert response["statusCode"] == 200
        assert response["body"] == mock_total_price
        
    def test_handler_exception(self, mocker):
        event = {"body": {"SPY": 2, "AAPL": 4}}
        mock_download = mocker.patch(
            "engine_lambda.main._download_tickets", side_effect=Exception("Error")
        )

        response = handler(event, {})

        mock_download.assert_called_once_with(event.get("body").keys())
        assert response["statusCode"] == 500
        assert response["body"] == "Internal Server Error"
