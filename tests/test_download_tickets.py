from numpy import float64
from engine_lambda.main import download_tickets, _extract_ticket, _extract_tickets
import numpy as np
from unittest.mock import ANY
import pandas as pd

class TestDownloadTicket:

    def test_download_one_ticket(self, mocker):
        input_ticket_numbers = ['SPY']
        mocker.patch("engine_lambda.main.yf.download")
        mock_extract_ticket = mocker.patch("engine_lambda.main._extract_ticket", return_value = {
            'SPY': np.float64(300)
        })

        response = download_tickets(input_ticket_numbers)
        
        assert response is not None
        assert type(response['SPY']) == float64
        mock_extract_ticket.assert_called_once_with(ANY, 'SPY')



    def test_download_multiple_tickes(self, mocker):
        input_ticket_numbers = ['SPY','NVDA']
        mocker.patch("engine_lambda.main.yf.download")

        mock_extract_tickets = mocker.patch("engine_lambda.main._extract_tickets", return_value = {
            'SPY': np.float64(300),
            'NVDA': np.float64(300)
        })

        response = download_tickets(input_ticket_numbers)
        
        assert response is not None
        assert type(response['SPY']) == float64
        assert type(response['NVDA']) == float64
        mock_extract_tickets.assert_called_once_with(ANY, input_ticket_numbers)
        
    def test_extract_ticket(self):
        data = {
            "Close": pd.Series([100, 200, 300], index=["2023-01-01", "2023-01-02", "2023-01-03"])
        }
        market_data = pd.DataFrame(data)
        ticket = "SPY"
        expected = {ticket: 300}
        
        result = _extract_ticket(market_data, ticket)
        
        assert result == expected

    def test_extract_tickets(self):
        market_data = pd.DataFrame({
            "SPY": [100, 200, 300],
            "AAPL": [150, 250, 350]
        }, index=["2023-01-01", "2023-01-02", "2023-01-03"])
        tickets = ["SPY", "AAPL"]
        expected = {
            "SPY": 300,
            "AAPL": 350
        }
        wrapped_market_data = {"Close": market_data}
        
        result = _extract_tickets(wrapped_market_data, tickets)

        assert result == expected