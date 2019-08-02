# OTPy (One-Time Password for Python)

## Introduction

This is a Python package to cater to all your needs for generatring and verifying OTP (One-Time Password). You can use this package to enable 2FA (2-Factor Authentication) to safeguard your web applications.

The package currently only supports TOTP (Time-based One-Time Password) according to the specifications in [RFC 6238](https://tools.ietf.org/html/rfc6238) and will support HOTP (HMAC-based One-Time Password) which is based on [RFC 4226](https://tools.ietf.org/html/rfc4226) soon. The package will also add support for generating the QR code for key URI in future releases.

This is a server-side implementation of the TOTP. For the client-side, the user can use any authentication applications (e.g. [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_SG), [Authy](https://authy.com/), etc.).
