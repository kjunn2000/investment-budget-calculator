from engine_lambda.main import handler
from test_base import TestBase


class TestHandler(TestBase):

    def test_handler_with_one_ticket(
        self, mocker, mock_latest_price, mock_total_price, mock_quantity_dict
    ):
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
