# OTPy (One-Time Password for Python)

## Introduction

This is a Python package to cater to all your needs for generating and verifying OTP (One-Time Password). You can use this package to enable 2FA (2-Factor Authentication) to safeguard your web applications.

The package currently only supports TOTP (Time-based One-Time Password) according to the specifications in [RFC 6238](https://tools.ietf.org/html/rfc6238) and will support HOTP (HMAC-based One-Time Password) which is based on [RFC 4226](https://tools.ietf.org/html/rfc4226) soon. The package will also add support for generating the QR code for key URI in future releases.

This is a server-side implementation of the TOTP. For the client-side, the user can use any authentication applications (e.g. [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_SG), [Authy](https://authy.com/), etc.).


## Installation

The package only supports Python 3.7 and above. To install:

```bash
pip install otpy
```

Alternatively,

```bash
python3 -m pip install otp
```

Optionally, if you are Under unix, you can install the `qrencode` package:

```bash
apt-get install qrencode
```

## Usage

This package is very simple to use. First, import the package:

```python
from otpy import OTPY
```

First, instantiate a TOTP object:

```python
key = "0123456789ABCDEF" # Key string must be hexadecimal!
otp = OTPY(key)
```

To get the Base32 encoded key value, simply run:

```python
otp.get_base32_key()
```

This value is compatible with apps like Google Authenticator and can be used to generate key URI.

To get the TOTP value:

```python
otp.get_totp()
```

Lastly, to verify if an OTP is correct, run:

```python
otp.verify_otp("123456")
```
