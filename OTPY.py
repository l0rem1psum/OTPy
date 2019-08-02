import hmac
import hashlib
import time
import base64

class OTPY(object):
    def __init__(self, key: str):
        self._key = key

    def _hex_str_2_bytes(self, hex: str) -> bytes:
        hex = '010' + hex if len(hex) & 1 else '10' + hex
        return bytes.fromhex(hex)[1:]

    def _hmac_sha(self, keyBytes: bytes, text: bytes) -> bytes:
        h_mac = hmac.new(keyBytes, text, hashlib.sha1)
        return h_mac.digest()

    def get_base32_Key(self) -> str:
        key_bytes = self._hex_str_2_bytes(self._key)
        return base64.b32encode(key_bytes)

    def get_totp(self, returnDigits: int = 6, T0: int = 0, X: int = 30) -> str:
        codeDigits = int(returnDigits)
        result = str()

        # Get the current time
        current_time = int(time.time())

        # Get the integer number of steps
        steps = (current_time - T0) // X

        # Get the hexadecimal value of the number of steps and remove the heading '0x'
        steps = hex(steps)[2:]

        # Pad zeros in the front
        steps = steps.zfill(16)

        msg = self._hex_str_2_bytes(steps)
        k = self._hex_str_2_bytes(self._key)
        sha_hash = self._hmac_sha(k, msg)

        # Dynamic Truncation
        # Find the last 4 bits as offset 
        offset = sha_hash[len(sha_hash) - 1] & 0xf

        # Find the DBC (Dynamic Binary Code) using the offset
        binary = (sha_hash[offset] & 0x7f) << 24
        binary |= (sha_hash[offset + 1] & 0xff) << 16
        binary |= (sha_hash[offset + 2] & 0xff) << 8
        binary |= (sha_hash[offset + 3] & 0xff)

        hotp = binary % (10**returnDigits)

        return str(hotp)


if __name__ == "__main__":

    key = "12345"
    otpy = OTPY(key)
    totp = otpy.get_totp()
    print(totp)

    print(otpy.get_base32_Key())
