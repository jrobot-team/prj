# -*- coding: utf-8 -*-

token = '_________'

WEBHOOK_HOST = '_______'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)


admin = (0,)

TIMEZONE = 'Europe/Moscow'

pagelimit = 10


prices_diap = [
    {'min': 0, 'max': 500000},
    {'min': 500000, 'max': 1500000},
    {'min': 1500000, 'max': 2000000},
    {'min': 2000000, 'max': 2500000},
    {'min': 2500000, 'max': 3000000},
    {'min': 3000000, 'max': 3500000},
    {'min': 3500000, 'max': 4000000},
    {'min': 4000000, 'max': 4500000},
    {'min': 4500000, 'max': 5000000},
    {'min': 5000000, 'max': 5500000},
    {'min': 5500000, 'max': 6000000},
    {'min': 6500000, 'max': 7000000},
    {'min': 7000000, 'max': 7500000},
    {'min': 7500000, 'max': 8000000},
    {'min': 8000000, 'max': 8500000},
    {'min': 8500000, 'max': 9000000},
    {'min': 9000000, 'max': 9500000},
    {'min': 9500000, 'max': 10000000},
]


tow_prices = {
    'troick': [
        (0, 4000000),
        (4000000, 5000000),
        (5000000, 6000000),
        (6000000, 7000000),
        (7000000, 8000000),
        (8000000, 9000000),
        (9000000, 0),
    ],
    'chehov': [
        (0, 1000000),
        (1000000, 2000000),
        (2000000, 2500000),
        (2500000, 3000000),
        (3000000, 3500000),
        (3500000, 4000000),
        (4000000, 0),
    ]
}
