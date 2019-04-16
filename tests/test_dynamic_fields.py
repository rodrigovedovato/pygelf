import logging
import pytest
from pygelf import GelfTcpHandler, GelfUdpHandler, GelfHttpHandler, GelfTlsHandler, GelfKafkaHandler, GelfKafkaHandler
from tests.helper import get_unique_message, log_warning


class DummyFilter(logging.Filter):
    def filter(self, record):
        record.ozzy = 'diary of a madman'
        record.van_halen = 1984
        record.id = 42
        return True


kafka_options = {
    "acks": 0,
    "linger_ms": 10,
    "max_block_ms": 5000
}


@pytest.fixture(params=[
    GelfTcpHandler(host='127.0.0.1', port=12201),
    GelfUdpHandler(host='127.0.0.1', port=12202),
    GelfUdpHandler(host='127.0.0.1', port=12202, compress=False),
    GelfHttpHandler(host='127.0.0.1', port=12203),
    GelfHttpHandler(host='127.0.0.1', port=12203, compress=False),
    GelfTlsHandler(host='127.0.0.1', port=12204),
    GelfKafkaHandler("localhost:9092", "logs", kafka_options, _facility="kfl", _origin="dev")
    # GelfTlsHandler(host='127.0.0.1', port=12204, validate=True, ca_certs='tests/config/cert.pem'),
])
def handler(request):
    return request.param


@pytest.yield_fixture
def logger(handler):
    logger = logging.getLogger('test')
    dummy_filter = DummyFilter()
    logger.addFilter(dummy_filter)
    logger.addHandler(handler)
    yield logger
    logger.removeHandler(handler)
    logger.removeFilter(dummy_filter)


def test_dynamic_fields(logger):
    message = get_unique_message()
    graylog_response = log_warning(logger, message, fields=['ozzy', 'van_halen'])
    assert graylog_response['message'] == message
    assert graylog_response['ozzy'] == 'diary of a madman'
    assert graylog_response['van_halen'] == 1984
    assert graylog_response['_id'] != 42
    assert 'id' not in graylog_response
