from numpy import float64
from engine_lambda.main import download_tickets

class TestDownloadTicket:

    def test_download_one_ticket(self, mocker):
        input_ticket_numbers = ['SPY']

        response = download_tickets(input_ticket_numbers)
        
        assert response is not None
        assert type(response['SPY']) == float64



    def test_download_multiple_tickes(self, mocker):
        input_ticket_numbers = ['SPY','NVDA']

        response = download_tickets(input_ticket_numbers)
        
        assert response is not None
        assert type(response['SPY']) == float64
        assert type(response['NVDA']) == float64
