import logging
import yfinance as yf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_tickets(tickets: list):
    ticketStr = " ".join(tickets)
    response = yf.download(ticketStr)
    return _extract_ticket(response, tickets[0]) if len(tickets) == 1 else _extract_tickets(response, tickets)


def _extract_ticket(market_data, ticket):
    response = {ticket: market_data["Close"].iloc[-1]}
    return response


def _extract_tickets(market_data, tickets):
    response = {}
    for ticket in tickets:
        response[ticket] = market_data["Close"][ticket].iloc[-1]
    return response
