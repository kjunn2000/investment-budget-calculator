from numpy import float64
from engine_lambda.main import (
    _download_tickets,
)
import numpy as np
from unittest.mock import ANY
from test_base import TestBase


class TestDownloadTicket(TestBase):

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