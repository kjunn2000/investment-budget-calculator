import logging
import yfinance as yf
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_tickets(tickets: list):
    ticketStr = " ".join(tickets)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    response = yf.download(ticketStr, start=yesterday, rounding=True)
    return _extract_ticket(response, tickets[0]) if len(tickets) == 1 else _extract_tickets(response, tickets)


def _extract_ticket(market_data, ticket):
    return {ticket: market_data["Close"].iloc[-1]}


def _extract_tickets(market_data, tickets):
    return { ticket: market_data["Close"][ticket].iloc[-1] for ticket in tickets}
