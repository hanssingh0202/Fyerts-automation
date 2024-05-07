import pyotp as tp

totp_key='HR6LFQJNMJ5FIHWZCUUK6GUQ2QJROFVL'
k = tp.TOTP(totp_key).now()
print(k)