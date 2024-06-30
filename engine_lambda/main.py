import logging
import yfinance as yf
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(event, _):
    try:

        body = event.get("body")
        latest_price = _download_tickets(body.keys())
        total_price = _calculate_latest_price(latest_price, body)
        return {
            "statusCode": 200,
            "body": total_price
        }
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 500,
            "body": "Internal Server Error"
        }


def _download_tickets(tickets: list):
    ticketStr = " ".join(tickets)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    response = yf.download(ticketStr, start=yesterday, rounding=True)
    return (
        _extract_ticket(response, tickets[0])
        if len(tickets) == 1
        else _extract_tickets(response, tickets)
    )


def _extract_ticket(market_data, ticket):
    return {ticket: market_data["Close"].iloc[-1]}


def _extract_tickets(market_data, tickets):
    return {ticket: market_data["Close"][ticket].iloc[-1] for ticket in tickets}


def _calculate_latest_price(latest_price, quantity_dict):
    data = {
        ticket: latest_price[ticket] * quantity_dict[ticket]
        for ticket in quantity_dict.keys()
    }
    total_price = sum(data.values())
    
    return {
        "data": data,
        "total": total_price
    }
