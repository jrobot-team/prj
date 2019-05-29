# -*- coding: utf-8 -*-

token = '_'

WEBHOOK_HOST = '_'
WEBHOOK_PORT = 88  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)

admin = (5675578, 253164289, 149597275, )
# admin = (5675578, 253164289, )

timezone = 'Asia/Yekaterinburg'

pagelimit = 10

key = 'dsfe(ke4m3_3Kd,cGs23&hImYU63bH7'

statuses = ['user', 'nopoller', 'group_admin', 'bot_admin']
