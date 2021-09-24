import pytest

from telliot.query import PriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry
from telliot.query import RequestId
from telliot.query_registry import query_registry

def test_request_id():

    # Construct from integer
    x = RequestId(5)

    assert str(x) == "0x0000000000000000000000000000000000000000000000000000000000000005"
    assert repr(x) == "RequestId('0x0000000000000000000000000000000000000000000000000000000000000005')"

    # Construct from hex string
    x = RequestId("0x0000000000000000000000000000000000000000000000000000000000000005")
    x = RequestId("0000000000000000000000000000000000000000000000000000000000000005")

    b = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000005")
    x = RequestId(b)

def test_request_id__eq__():

    x = RequestId(5)
    assert x == 5
    assert x == RequestId(5)
    assert x == "0000000000000000000000000000000000000000000000000000000000000005"




def test_oracle_price_query():
    q = PriceQuery(RequestId(1), "eth", "usd", PriceType.current)
    assert q.uid == "current-price-eth-in-usd"
    assert q.question == "What is the current price of ETH in USD?"


def test_registry_creation():
    qr = QueryRegistry(_queries={})

    q1 = PriceQuery(RequestId(1), "eth", "usd", PriceType.current)
    q2 = PriceQuery(RequestId(2), "btc", "usd", PriceType.current)

    qr.register(q1)
    qr.register(q2)

    # Demonstrate getting query by Unique data spec ID
    query = qr.queries["current-price-eth-in-usd"]
    assert query is q1

    # Demonstrate getting query by Request ID
    query = qr.get_query_by_request_id(RequestId(2))
    assert query is q2

    # Key error
    with pytest.raises(KeyError):
        query = qr.queries["does-not-exist"]

    # Avoid duplicate request IDs
    with pytest.raises(ValueError):
        qr.register(PriceQuery(RequestId(2), "btc", "usd", PriceType.current))

    # Avoid duplicate UIDs
    with pytest.raises(ValueError):
        qr.register(PriceQuery(RequestId(3), "btc", "usd", PriceType.current))

def test_registry():

    q = query_registry.get_query_by_request_id(1)
    assert q.asset == 'eth'