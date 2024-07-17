import unittest
from unittest import mock

from libpurecool.dyson import DysonAccount, DysonNotLoggedInException
from libpurecool.dyson_pure_cool import DysonPureCool

API_HOST = 'appapi.cp.dyson.com'
API_CN_HOST = 'appapi.cp.dyson.cn'


class MockRequestResponse:
    def __init__(self, json, status_code=200, reason="OK"):
        self.text = json
        self.status_code = status_code
        self.reason = reason

    def json(self, **kwargs):
        return self.text


_mocked_login_post_response = MockRequestResponse(
    '{"account": "account", "token": "token", "tokenType": "Bearer"}'
)

_mocked_login_post_failed_response = MockRequestResponse(
    '{}',
    status_code=401,
    reason='Unauthorized'
)

_mocked_device_list = MockRequestResponse(
    [
        {
            "Serial": "serial-1",
            "Name": "device-1",
            "Version": "1",
            "AutoUpdate": True,
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                "bCm7uYeTORULKLKQ==",
            "NewVersionAvailable": False,
            "ProductType": "358"
        }
    ]
)


def _mock_path_write(text):
    """Do nothing.

    Prevents overwriting existing cached credentials when unittests run.
    """
    pass


class TestDysonAccount(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('libpurecool.dyson.Path.read_text')
    @mock.patch('libpurecool.dyson.Path.write_text', side_effect=_mock_path_write)
    @mock.patch('builtins.input')
    @mock.patch('libpurecool.dyson.DysonAccount._get_challenge')
    @mock.patch('libpurecool.dyson.Path.exists')
    @mock.patch('libpurecool.dyson.requests.post')
    def test_connect_account(self, mocked_login, mocked_path_exists, mocked_challenge, mocked_pin_input,
                             mocked_path_write, mocked_path_read):
        mocked_login.return_value = _mocked_login_post_response
        mocked_path_exists.return_value = False
        mocked_challenge.return_value = "challenge"
        mocked_pin_input.return_value = "123456"
        mocked_path_read.return_value = _mocked_login_post_response.text
        dyson_account = DysonAccount("email", "password", "language")
        dyson_account.login()
        self.assertEqual(mocked_login.call_count, 1)
        self.assertEqual(mocked_path_write.call_count, 1)
        self.assertEqual(mocked_path_read.call_count, 1)
        self.assertIsInstance(dyson_account._token, str)

    @mock.patch('builtins.input')
    @mock.patch('libpurecool.dyson.DysonAccount._get_challenge')
    @mock.patch('libpurecool.dyson.Path.exists')
    @mock.patch('libpurecool.dyson.requests.post')
    def test_connect_account_failed(self, mocked_login, mocked_path_exists, mocked_challenge, mocked_pin_input):
        mocked_login.return_value = _mocked_login_post_failed_response
        mocked_path_exists.return_value = False
        mocked_challenge.return_value = "challenge"
        mocked_pin_input.return_value = "123456"
        dyson_account = DysonAccount("email", "password", "language")
        self.assertRaises(DysonNotLoggedInException, dyson_account.login)
        self.assertEqual(mocked_login.call_count, 1)
        self.assertIsNone(dyson_account._token, str)

    @mock.patch('libpurecool.dyson.Path.exists')
    @mock.patch('libpurecool.dyson.requests.post')
    def test_connect_account_cached_credentials(self, mocked_login, mocked_path_exists):
        mocked_login.return_value = _mocked_login_post_response
        mocked_path_exists.return_value = True
        dyson_account = DysonAccount("email", "password", "language")
        dyson_account.login()
        self.assertEqual(mocked_login.call_count, 0)
        self.assertIsInstance(dyson_account._token, str)

    def test_process_http_response(self):
        dyson_account = DysonAccount("email", "password", "language")
        response = mock.Mock()
        response.status_code = 200
        response.reason = "OK"
        response.text = "response"
        self.assertEqual(dyson_account.process_http_response(response), "response")

    def test_process_http_response_failed(self):
        dyson_account = DysonAccount("email", "password", "language")
        response = mock.Mock()
        response.status_code = 401
        response.reason = "Unauthorized"
        response.text = "response"
        self.assertRaises(DysonNotLoggedInException, dyson_account.process_http_response, response)

    @mock.patch('libpurecool.dyson.Path.exists')
    @mock.patch('libpurecool.dyson.requests.get')
    @mock.patch('libpurecool.dyson.requests.post')
    def test_list_devices(self, mocked_login, mocked_list_devices, mocked_path_exists):
        mocked_login.return_value = _mocked_login_post_response
        mocked_list_devices.return_value = _mocked_device_list
        dyson_account = DysonAccount("email", "password", "language")
        mocked_path_exists.return_value = True
        dyson_account.login()
        self.assertEqual(mocked_path_exists.call_count, 1)
        self.assertEqual(mocked_login.call_count, 0)
        devices = dyson_account.devices()
        self.assertEqual(mocked_list_devices.call_count, 1)
        self.assertEqual(len(devices), 1)
        self.assertTrue(isinstance(devices[0], DysonPureCool))
        self.assertTrue(devices[0].auto_update)
        self.assertFalse(devices[0].new_version_available)
        self.assertEqual(devices[0].serial, 'serial-1')
        self.assertEqual(devices[0].name, 'device-1')
        self.assertEqual(devices[0].version, '1')
        self.assertEqual(devices[0].product_type, '358')
        self.assertEqual(devices[0].credentials, 'password1')
