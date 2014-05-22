
Flask-APNS
==========

**Flask-APNS** allows Flask to send APNS messages easily. It's a simple extension to configure http://apns-client.readthedocs.org

User's Guide
------------

Simple flask app ::


    app = Flaks(__name__)
    apns = APNS(app, cert_string='XXX', key_string='XXX')
    apns.send_message(['token1', 'token2', 'token3'], 'hello world')

Application factory ::

    apns = APNS()

    def create_app():
        app = Flaks(__name__)
        app.config['APNS_ADDRESS'] = 'push_sandbox'
        app.config['APNS_CERT_STRING'] = 'XXX'
        app.config['APNS_KEY_STRING'] = 'XXX'

        apns.init_app(app)

        return app

API
---

.. autoclass:: flask_apns.APNS
    :members:
    :special-members: __init__


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

