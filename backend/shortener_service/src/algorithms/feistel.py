class FeistelCipher:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def feistel_encrypt(self, snowflake_id):
        left_part = snowflake_id >> 32
        right_part = snowflake_id & 0xFFFFFFFF

        for i in range(8):
            round_key = (self.secret_key + i) & 0xFFFFFFFF
            f_result = ((right_part ^ round_key) * 4294967291) & 0xFFFFFFFF
            left_part, right_part = right_part, left_part ^ f_result

        return (left_part << 32 | right_part) & 0xFFFFFFFFFFFFFFFF

    def feistel_decrypt(self, encrypted_id):
        left_part = encrypted_id >> 32
        right_part = encrypted_id & 0xFFFFFFFF

        for i in reversed(range(8)):
            round_key = (self.secret_key + i) & 0xFFFFFFFF
            f_result = ((right_part ^ round_key) // 4294967291) & 0xFFFFFFFF
            right_part, left_part = right_part, left_part ^ f_result

        return (left_part << 32 | right_part) & 0xFFFFFFFFFFFFFFFF
