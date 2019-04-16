import pytest
from pygelf import GelfTcpHandler, GelfUdpHandler, GelfHttpHandler, GelfTlsHandler, GelfKafkaHandler
from tests.helper import logger, get_unique_message, log_warning

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


def test_debug_mode(logger):
    message = get_unique_message()
    graylog_response = log_warning(logger, message)
    assert graylog_response['message'] == message
    assert graylog_response['file'] == 'helper.py'
    assert graylog_response['module'] == 'helper'
    assert graylog_response['func'] == 'log_warning'
    assert graylog_response['logger_name'] == 'test'
    assert 'line' in graylog_response
