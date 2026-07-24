import time
import threading

DATACENTER_ID = 1
WORKER_ID = 1
FEISTEL_SECRET_KEY = 248937142


class SnowflakeGenerator:
    def __init__(self, datacenter_id, worker_id) -> None:
        self.dc_id = datacenter_id & 0x1F
        self.worker_id = worker_id & 0x1F
        self.sequence = 0
        self.last_ts = 0
        self._lock = threading.Lock()
        self.EPOCH = 1609459200000

    def _current_timestamp(self) -> int:
        return int(time.time() * 1000)
     
    def _wait_next_millis(self, last_ts) -> int:
        ts = self._current_timestamp()
        while ts <= last_ts:
            ts = self._current_timestamp()
        return ts

    def next_id(self):
        with self._lock:
            ts = self._current_timestamp()
            if ts == self.last_ts:
                self.sequence = (self.sequence + 1) & 0xFFF
                if self.sequence == 0:
                    ts = self._wait_next_millis(self.last_ts)
            else:
                self.sequence = 0
                self.last_ts = ts
        snowflake = ((ts - self.EPOCH) << 22) | self.dc_id << 17 | self.worker_id << 12 | self.sequence
        return snowflake


class Feistel:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def feistel_encrypt(self, base62_num):
        left_part = base62_num >> 32
        right_part = base62_num & 0xFFFFFFFF

        for i in range(8):
            round_key = (self.secret_key + i) & 0xFFFFFFFF
            f_result = ((right_part ^ round_key) * 4294967291) & 0xFFFFFFFF
            left_part, right_part = right_part, left_part ^ f_result

        return (left_part << 32 | right_part) & 0xFFFFFFFFFFFFFFFF

    def feistel_decrypt(self, base62_num):
        left_part = base62_num >> 32
        right_part = base62_num & 0xFFFFFFFF

        for i in reversed(range(8)):
            round_key = (self.secret_key + i) & 0xFFFFFFFF
            f_result = ((right_part ^ round_key) // 4294967291) & 0xFFFFFFFF
            right_part, left_part = right_part, left_part ^ f_result

        return (left_part << 32 | right_part) & 0xFFFFFFFFFFFFFFFF


class UrlShortener:
    def __init__(self) -> None:
        self.base62_alphabet = "uLJGIBVXyzK9Nodaj3Tq4sAgMpUO0kPvSfQnCZicWtDmx2Rb5Yrh6w8EFHl17e"
        self.base_url = "https://pet.shortener/"

    def _ecnode_base62(self, unique_id: int) -> str:
        if unique_id == 0:
            return self.base62_alphabet[0]

        result: list[str] = []

        while unique_id > 0:
            remainder = unique_id % 62
            result.append(self.base62_alphabet[remainder])
            unique_id //= 62

        return ''.join(result[::-1])

    def _decode_base62(self, encoded_id: str) -> int:
        result: int = 0
        for char in base62_num:
            result = result * 62 + self.base62_alphabet.index(char)
        return result

    def create_short_url(self, unique_id: int) -> str:
        short_url = self._ecnode_base62(unique_id)
        return self.base_url + short_url

    def parse_short_url(self, short_url: str, feistel) -> int:
        short_code  = short_url.rstrip("/").rsplit("/", 1)[-1]
        encrypted_id = self._decode_base62(short_code)
        snowflake_id = feistel.feistel_decrypt(encrypted_id)
        return snowflake_id



snowflake = SnowflakeGenerator(DATACENTER_ID, WORKER_ID)
snowflake_id = snowflake.next_id()
print(f"Cнежинка: {snowflake_id}")

feistel = Feistel(FEISTEL_SECRET_KEY)
shuffle_id = feistel.feistel_encrypt(snowflake_id)
print(f"Шафл: {shuffle_id}")

shortener = UrlShortener()
base62_num = shortener._ecnode_base62(shuffle_id)
print(f"В base62: {base62_num}")
print(f"Из base62: {shortener._decode_base62(base62_num)}")

short_url = shortener.create_short_url(shuffle_id)
print(f"shorturl {short_url}")
print(f"Обратно полученный айди {shortener.parse_short_url(short_url, feistel)}")