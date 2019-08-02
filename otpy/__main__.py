from otpy import OTPY

if __name__ == "__main__":

    key = "12345DEADBEEF"
    otpy = OTPY(key)
    totp = otpy.get_totp()
    encoded_key = otpy.get_base32_key().decode("utf-8")
    print("The test key is {} with Base32 encoded value of {}.".format(key, encoded_key))
    print("Scan the following QR code with an authenticator app (e.g. Google Authenticator)")

    import subprocess, datetime
    uri = "otpauth://totp/Test?secret=" + encoded_key
    subprocess.run(["qrencode", "-t", "utf8", uri])

    print("The TOTP now (i.e. {}) is {}".format(datetime.datetime.now(), totp))