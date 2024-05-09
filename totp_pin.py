import pyotp as tp

totp_key=''#your top key
k = tp.TOTP(totp_key).now()
print(k)