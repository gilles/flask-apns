# coding=utf-8
import unittest
import tempfile
from apnsclient import Result

from flask import Flask
import minimock

import flask_apns


class APNSTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.tt = minimock.TraceTracker()

    def tearDown(self):
        minimock.restore()

    def test_init_with_params(self):
        minimock.mock('flask_apns.Certificate', returns='mocked_certificate',
                      tracker=self.tt)

        apns = flask_apns.APNS(self.app, cert_string='cert_string',
                               cert_file='cert_file', key_string='key_string',
                               key_file='key_file',
                               passphrase='passphrase')

        self.assertEqual(apns._certificate, 'mocked_certificate')

        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called flask_apns.Certificate(",
            "   cert_file='cert_file',",
            "   cert_string='cert_string',",
            "   key_file='key_file',",
            "   key_string='key_string',",
            "   passphrase='passphrase')"
        ]))

    def test_init_with_config(self):
        minimock.mock('flask_apns.Certificate', returns='mocked_certificate',
                      tracker=self.tt)

        self.app.config['APNS_ADDRESS'] = 'address'
        self.app.config['APNS_CERT_STRING'] = 'config_cert_string'
        self.app.config['APNS_CERT_FILE'] = 'config_cert_file'
        self.app.config['APNS_KEY_STRING'] = 'config_key_string'
        self.app.config['APNS_KEY_FILE'] = 'config_key_file'
        self.app.config['APNS_PASSPHRASE_STRING'] = 'config_passphrase'

        apns = flask_apns.APNS(self.app, cert_string='cert_string',
                               cert_file='cert_file', key_string='key_string',
                               key_file='key_file',
                               passphrase='passphrase')

        self.assertEqual(apns._certificate, 'mocked_certificate')

        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called flask_apns.Certificate(",
            "   cert_file='config_cert_file',",
            "   cert_string='config_cert_string',",
            "   key_file='config_key_file',",
            "   key_string='config_key_string',",
            "   passphrase='config_passphrase')"
        ]))

    def test_init_with_passphrase_file(self):
        minimock.mock('flask_apns.Certificate', returns='mocked_certificate',
                      tracker=self.tt)

        with tempfile.NamedTemporaryFile() as temp:
            temp.write('file_passphrase')
            temp.flush()

            self.app.config['APNS_PASSPHRASE_FILE'] = temp.name

            apns = flask_apns.APNS(self.app, cert_string='cert_string',
                                   cert_file='cert_file',
                                   key_string='key_string', key_file='key_file')

        self.assertEqual(apns._certificate, 'mocked_certificate')

        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called flask_apns.Certificate(",
            "   cert_file='cert_file',",
            "   cert_string='cert_string',",
            "   key_file='key_file',",
            "   key_string='key_string',",
            "   passphrase='file_passphrase')"
        ]))

    def test_send_disabled(self):
        minimock.mock('flask_apns.Certificate', returns='mocked_certificate',
                      tracker=self.tt)

        mocked_session = minimock.Mock('Session', tracker=self.tt)
        minimock.mock('flask_apns.Session', returns=mocked_session,
                      tracker=self.tt)

        apns = flask_apns.APNS(self.app, cert_string='cert_string',
                               cert_file='cert_file', key_string='key_string',
                               key_file='key_file')

        ret = apns.send_message('1234', 'alert')

        self.assertIsNone(ret)

    def test_send(self):
        minimock.mock('flask_apns.Certificate', returns='mocked_certificate')

        mocked_session = minimock.Mock('Session', tracker=self.tt)
        mocked_session.get_connection.mock_returns = "mocked_connection"
        minimock.mock('flask_apns.Session', returns=mocked_session)

        mocked_apns = minimock.Mock('APNs', tracker=self.tt)
        result = Result("done")
        mocked_apns.send.mock_returns = result
        minimock.mock('flask_apns.APNs', returns=mocked_apns,
                      tracker=self.tt)

        apns = flask_apns.APNS(self.app, cert_string='cert_string',
                               cert_file='cert_file', key_string='key_string',
                               key_file='key_file')

        ret = apns.send_message('1234', 'alert')

        self.assertIs(ret, result)

        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called Session.get_connection('push_sandbox', "
            "'mocked_certificate')",
            "Called flask_apns.APNs('mocked_connection')",
            "Called APNs.send(<apnsclient.apns.Message object at ...>)"
        ]))
