# coding=utf-8
"""
Send APNS message with flask
"""

from apnsclient import Session, Certificate, Message, APNs


class APNS(object):
    """
    APNS extension
    """

    def __init__(self, app=None, address="push_sandbox", failure_callback=None,
                 **cert_params):
        """
        :param app: The app to init
        :param address: The APNS address as understood by
            :py:meth:`apnsclient.apns.Session.get_connection`
        :param failure_callback: Called when calls to
            :py:meth:`apnsclient.apns.APNs.send` returns failures
        :param cert_params: Parameters to initialize
            :py:class:`apnsclient.apns.Certificate`
        """

        self.session = Session()

        self.failed_callback = failure_callback

        self._cert_params = cert_params
        self._address = address
        self._certificate = None

        if app is not None:
            self.session = self.init_app(app)

    def init_app(self, app):
        """
        Init the flask app. Tries to get parameters from the flask config,
        if not take them from the default ones passed in the constructor.

        Available flask config:

            * APNS_ADDRESS
            * APNS_CERT_STRING
            * APNS_CERT_FILE
            * APNS_KEY_STRING
            * APNS_KEY_FILE
            * APNS_PASSPHRASE_STRING
            * APNS_PASSPHRASE_FILE

        :param app: The app to init
        """
        if app.config.get('APNS_ADDRESS'):
            self._address = app.config.get('APNS_ADDRESS')

        cert_def = {}
        for key in (
                'cert_string', 'cert_file', 'key_string', 'key_file',
                'passphrase'):
            cert_def[key] = app.config.get(
                'APNS_%s' % key.upper()) or self._cert_params.get(key)

        # Handle PASSPHRASE_STRING vs PASSPHRASE_FILE
        # This is easier for dev vs. conf file vs. env based deployment
        # such as Heroku

        cert_def['passphrase'] = app.config.get(
            'APNS_PASSPHRASE_STRING') or self._cert_params.get('passphrase')
        if not cert_def['passphrase']:
            passphrase_file = app.config.get('APNS_PASSPHRASE_FILE')
            if passphrase_file:
                try:
                    with open(passphrase_file) as f:
                        cert_def['passphrase'] = f.read().strip()
                except IOError:
                    pass

        try:
            self._certificate = Certificate(**cert_def)
        except Exception as e:
            print("APNS is disabled: %r" % e)

        return self.session

    def get_connection(self):
        """
        Get a connection to APNS

        :returns: :py:class:`apnsclient.apns.Connection`
        """
        if self._certificate is None:
            return None
        return self.session.get_connection(self._address, self._certificate)

    def send_message(self, tokens, alert=None, badge=None, sound=None,
                     expiry=None, payload=None, **extra):
        """
        Send a message. This will not retry but will call the
            failed_callback in case of failure

        .. seealso::

            :py:class:`apnsclient.apns.Message` for a better description of the
                parameters

        :param tokens: The tokens to send to
        :param alert: The alert message
        :param badge: The badge to show
        :param sound: The sound to play
        :param expiry: A timestamp when message will expire
        :param payload: The payload
        :param extra: Extra info

        """
        connection = self.get_connection()
        if connection is None:
            return None

        if not tokens:
            return False

        message = Message(tokens, alert, badge, sound, expiry, payload,
                          **extra)
        srv = APNs(connection)
        res = srv.send(message)
        if res.failed and self.failed_callback:
            for key, reason in res.failed.iterkeys():
                self.failed_callback(key, reason)
        return res
