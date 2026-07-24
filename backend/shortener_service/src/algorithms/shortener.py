from src.algorithms.feistel import FeistelCipher


class UrlShortener:
    def __init__(self, base_url: str, feistel: FeistelCipher) -> None:
        self.base62_alphabet = "uLJGIBVXyzK9Nodaj3Tq4sAgMpUO0kPvSfQnCZicWtDmx2Rb5Yrh6w8EFHl17e"
        self.base_url = base_url
        self.feistel = feistel

    def _encode_base62(self, encrypted_id: int) -> str:
        if encrypted_id == 0:
            return self.base62_alphabet[0]

        result: list[str] = []

        while encrypted_id > 0:
            remainder = encrypted_id % 62
            result.append(self.base62_alphabet[remainder])
            encrypted_id //= 62

        return ''.join(result[::-1])

    def _decode_base62(self, short_code: str) -> int:
        result: int = 0
        for char in short_code:
            result = result * 62 + self.base62_alphabet.index(char)
        return result

    def create_short_code(self, snowflake_id: int) -> str:
        encrypted_id = self.feistel.feistel_encrypt(snowflake_id)
        short_code = self._encode_base62(encrypted_id)
        return short_code

    def create_short_url(self, short_code: str) -> str:
        return self.base_url + "/" + short_code
