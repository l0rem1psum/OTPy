import hmac
import hashlib
import time
import base64

class OTPY(object):
    """OTPY class for generating One-Time Password (OTP)"""

    def __init__(self, key: str):
        """
        Args:
            key (str): A hexadecimal key string.

        """
        self._key = key

    def _hex_str_2_bytes(self, hex: str) -> bytes:
        """ Method to convert a hexadecimal string to `bytes` built-in type.

        Args:
            hex (str): Hexadecimal string.

        Returns:
            bytes: Converted hexadecimal string.

        """
        hex = '010' + hex if len(hex) & 1 else '10' + hex
        return bytes.fromhex(hex)[1:]

    def _hmac_sha(self, keyBytes: bytes, text: bytes) -> bytes:
        """ Method to obtain the digest of the Key-Hashed Message Authentication Code.

        Currently only support HMAC-SHA1 based on the specifications in RFC 2104.

        Args:
            keyBytes (bytes): The secret key.
            text (bytes): The message to be authenticated.

        Returns:
            bytes: A 20-byte long `bytes` type hash output. The output byte-length depends on the length of the hash function.
        
        """
        h_mac = hmac.new(keyBytes, text, hashlib.sha1)
        return h_mac.digest()

    def get_base32_key(self) -> str:
        """ Method to convert the secret key to a Base32 encoded key based on the specificatiosn in RFC 3548. 
        
        Returns:
            str: The Base32 encoded secret key.
        
        """
        key_bytes = self._hex_str_2_bytes(self._key)
        return base64.b32encode(key_bytes)

    def get_totp(self, returnDigits: int = 6, T0: int = 0, X: int = 30) -> str:
        """ Get the TOTP at the current time.

        Args:
            returnDigits (int): Number of digits of the TOTP. Default is 6.
            T0 (int): The Unix time to start counting time steps (default value is 0, i.e., the Unix epoch).
            X: the time step in seconds (default value X = 30 seconds).

        Returns:
            str: TOTP of length returnDigits.
        
        """
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

        return str(hotp).zfill(returnDigits)

    def verify_otp(self, otp: str) -> bool:
        """ Verify the OTP given

        Returns:
            bool: True if the OTP is correct, False if wrong
        
        """
        return otp == self.get_totp()
        